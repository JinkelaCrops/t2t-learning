import re
from typing import Callable


def _flatten_region_to_region(flatten_region, strip=True):
    if strip:
        if len(flatten_region) > 0 and flatten_region[0] == flatten_region[1]:
            flatten_region = flatten_region[2:]
        if len(flatten_region) > 0 and flatten_region[-1] == flatten_region[-2]:
            flatten_region = flatten_region[:-2]
    if len(flatten_region) % 2 > 0:
        flatten_region.pop(-1)
    region = []
    for i in range(len(flatten_region) // 2):
        region.append(flatten_region[2 * i: 2 * i + 2])
    return region


def gen_unmasked_region(mask: list):
    mask_region_tmp = [0]
    continue_flag = False
    for k, current_state in enumerate(mask):
        if continue_flag ^ current_state:
            continue_flag = not continue_flag
            mask_region_tmp.append(k)
    if continue_flag and continue_flag:
        mask_region_tmp.append(len(mask))
    mask_region_tmp.append(len(mask))
    mask_region = _flatten_region_to_region(mask_region_tmp)
    return mask_region


def mask_update(mask, pts: dict):
    if not pts:
        return
    for i, pti in pts.items():
        for j in pti:
            for k in range(j[0], j[1]):
                mask[k] = 1


def pattern_sub_pts(regex, replace, sent, flags=0, group=0, mask=None) -> str:
    if "(?=" in regex or "(?!" in regex:
        raise Exception("do not support look ahead, for finditer will block all str behind endpos")
    if isinstance(replace, str) and re.search("\\\\[0-9]", replace):
        raise Exception("do not support group replacement while replace is str, use Callable instead")
    mask = [0] * len(sent) if mask is None else mask
    unmasked_region = gen_unmasked_region(mask)
    output = {}
    p = re.compile(regex, flags=flags)
    for region in unmasked_region:
        for x in p.finditer(sent, region[0], region[1]):
            position = x.span()
            pattern = x.group(group)
            pattern_sub = ""
            if isinstance(replace, str):
                pattern_sub = replace
            elif isinstance(replace, Callable):
                pattern_sub = replace(x)
            output[position] = pattern_sub
    output_str = ""
    last_pos = 0
    for pos in sorted(list(output.keys())):
        output_str += sent[last_pos:pos[0]] + output[pos]
        last_pos = pos[1]
    output_str += sent[last_pos:len(sent)]
    return output_str


def pattern_find_pts(regex, sent, flags=0, group=0, mask=None) -> dict:
    if "(?=" in regex or "(?!" in regex:
        raise Exception("do not support look ahead, for finditer will block all str behind endpos")
    mask = [0] * len(sent) if mask is None else mask
    unmasked_region = gen_unmasked_region(mask)
    output = {}
    p = re.compile(regex, flags=flags)
    for region in unmasked_region:
        for x in p.finditer(sent, region[0], region[1]):
            position = [x.start(), x.end()]
            pattern = x.group(group)
            if pattern in output:
                output[pattern].append(position)
            else:
                output[pattern] = [position]
    return output
