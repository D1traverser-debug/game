#!/usr/bin/env python3
"""Mechanical cross-conversation checkpoint guard; NOT a game-quality test."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import sys

OWNER_SCOPE={
    'product':'original-IP full-game 3D co-op roguelite inspired by The Spell Brigade gameplay',
    'modes':['solo','online_coop_1_to_4'],
    'players':'1-4',
    'multiplayer':True,
    'target_platform':'Windows PC first',
    'input':['keyboard_mouse','controller'],
    'engine':'Unity 6.3 LTS + URP (selected for vertical-slice validation)',
    'final_delivery':'native Windows PC build; Steam distribution target',
    'original_ip_required':True,
}

def verify(root:Path)->dict:
    state_path=root/'docs'/'PROJECT_STATE.json'
    source_path=root/'index.html'
    handoff=root/'HANDOFF.md'
    findings=[]
    try:
        state=json.loads(state_path.read_text(encoding='utf-8'))
    except (ValueError,OSError) as exc:
        return {'status':'FAIL','errors':[f'STATE_MISSING_OR_INVALID:{exc}']}
    if state.get('repository')!='D1traverser-debug/game':
        findings.append('WRONG_REPOSITORY')
    if state.get('active_production_branch')!='full-game' or state.get('branch')!='full-game':
        findings.append('ACTIVE_BRANCH_DRIFT')
    legacy=state.get('legacy_browser_prototype',{})
    if legacy.get('branch')!='development':
        findings.append('LEGACY_PROTOTYPE_BRANCH_DRIFT')
    for key,want in OWNER_SCOPE.items():
        if state.get('scope',{}).get(key)!=want:
            findings.append(f'SCOPE_DRIFT:{key}')
    if state.get('caos_boundary','').lower().find('read-only')<0:
        findings.append('CAOS_READ_ONLY_BOUNDARY_MISSING')
    if state.get('status')=='READY' and not state.get('owner_acceptance'):
        findings.append('UNSUPPORTED_READY_STATUS')
    try:
        contents=source_path.read_bytes()
    except OSError as exc:
        return {'status':'FAIL','errors':[f'SOURCE_MISSING:{exc}']+findings}
    digest=hashlib.sha256(contents).hexdigest()
    expected=legacy.get('sha256') or state.get('development_candidate_sha256')
    if not expected:
        findings.append('LEGACY_ARTIFACT_SHA_MISSING')
    elif digest!=expected:
        findings.append('ARTIFACT_SHA_MISMATCH')
    expected_bytes=legacy.get('bytes') or state.get('development_candidate_bytes')
    if expected_bytes!=len(contents):
        findings.append('LEGACY_ARTIFACT_SIZE_MISMATCH')
    text=contents.decode('utf-8','replace')
    if '<script>' not in text or '</script>' not in text or '<style>' not in text:
        findings.append('NOT_SINGLE_FILE_HTML')
    if 'window.__QA' in text:
        findings.append('PRODUCTION_DEBUG_MUTATION_SURFACE')
    if any(marker in text for marker in ['<script src=', '<link rel="stylesheet" href=', '<iframe src=']):
        findings.append('EXTERNAL_RUNTIME_ASSET_FOUND')
    if not handoff.exists():
        findings.append('HANDOFF_MISSING')
    return {
        'status':'PASS_MECHANICAL_ONLY' if not findings else 'FAIL',
        'sha256':digest,
        'bytes':len(contents),
        'checkpoint':state.get('checkpoint'),
        'active_branch':state.get('active_production_branch'),
        'product_status':state.get('status'),
        'legacy_artifact_sha256':digest,
        'errors':findings,
        'warning':'This verifies full-game scope metadata and legacy HTML artifact integrity only. It does not verify a Unity project/build, gameplay, networking, art/audio, performance, persistence or player acceptance.'
    }

def main()->int:
    parser=argparse.ArgumentParser()
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    args=parser.parse_args()
    result=verify(args.root)
    print(json.dumps(result,indent=2,ensure_ascii=False))
    return 0 if result['status']=='PASS_MECHANICAL_ONLY' else 1

if __name__=='__main__':
    sys.exit(main())
