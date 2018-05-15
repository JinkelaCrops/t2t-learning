import unicodedata
import re


def omit_blank_join(sep, iterable, format=None):
    out = ""
    if format is None:
        format = "%s"
    for it in iterable:
        if len(it) == 0:
            continue
        out += format % it + sep
    if len(out) > 0:
        out = out[0:len(out) - len(sep)]
    return out


def interval_merge(intervals, surplus=1):
    # input intervals, output merged intervals
    # [[1,5], [1,2], [3,3], [1,1], [2,6], [8,10], [11,12]] -> [1,6] [8,10] [11,12]
    # sort and update, better idea?
    output_intervals = []
    sorted_intervals = sorted(intervals)
    i = 0
    sn = sorted_intervals[0]
    while i < len(sorted_intervals) - 1:
        s1 = sorted_intervals[i + 1]
        if s1[1] <= sn[1]:
            i += 1
        elif s1[0] <= sn[1] + surplus:
            sn = [sn[0], s1[1]]
            i += 1
        else:
            output_intervals.append(sn)
            sn = s1
            i += 1
    output_intervals.append(sn)
    return output_intervals


def char_to_unicode(char):
    return "\\u" + ("0000" + hex(ord(char))[2:])[-4:]


def unicode_to_char(char):
    return chr(int(char.strip("\\u"), 16))


def string_to_unicode(input):
    output = ""
    for s in input:
        output += char_to_unicode(s)
    return output


def unicode_to_string(input):
    output = ""
    for s in input.split("\\u"):
        if len(s) == 0:
            continue
        output += unicode_to_char(s)
    return output


def unicode_to_num(unicode):
    return int(unicode[2:], 16)


def num_to_unicode(num):
    if len(hex(num)) <= 6:
        return "\\u" + ("0000" + hex(num)[2:])[-4:]
    else:
        return "\\U" + ("00000000" + hex(num)[2:])[-8:]


def char_to_num(char):
    return ord(char)


def interval_expr_to_unicode(input_intervals):
    output_intervals = []

    for input_interval in input_intervals:
        if input_interval == "":
            continue
        if "-" in input_interval and "\\u" in input_interval:
            interval_tmp = input_interval.split("-")
            interval_tmp = [unicode_to_num(interval_tmp[0]), unicode_to_num(interval_tmp[1])]
            output_intervals.append(interval_tmp)
        elif len(input_interval) == 3 and input_interval[1:2] == "-":
            interval_tmp = input_interval.split("-")
            interval_tmp = [char_to_num(interval_tmp[0]), char_to_num(interval_tmp[1])]
            output_intervals.append(interval_tmp)
        elif "\\u" in input_interval:
            for c in input_interval.split("\\u"):
                if c == "":
                    continue
                ci = [int(c, 16), int(c, 16)]
                output_intervals.append(ci)
        else:
            for c in input_interval:
                ci = [char_to_num(c), char_to_num(c)]
                output_intervals.append(ci)
    output_intervals = interval_merge(output_intervals, 1)

    single_unicode = []
    merged_unicode = []
    for output_interval in output_intervals:
        if output_interval[0] == output_interval[1]:
            single_unicode.append(num_to_unicode(output_interval[0]))
        else:
            merged_unicode.append(num_to_unicode(output_interval[0]) + "-" + num_to_unicode(output_interval[1]))
    if len(single_unicode) > 0:
        merged_unicode.append("".join(single_unicode))

    return merged_unicode


def interval_unicode_to_char(interval_patterns):
    output = []
    for interval_pattern in interval_patterns:
        if "-" in interval_pattern and "\\u" in interval_pattern:
            interval_tmp = interval_pattern.split("-")
            for i in range(int(interval_tmp[0][2:], 16), int(interval_tmp[1][2:], 16) + 1):
                output.append(chr(i))
        elif "\\u" in interval_pattern:
            for i in interval_pattern.split("\\u"):
                if len(i) == 0:
                    continue
                output.append(chr(int(i, 16)))
    return output


def expr_converter(input_expr):
    interval_regex = "\\\\u[a-zA-Z0-9]{4}\-\\\\u[a-zA-Z0-9]{4}"
    interval_patterns = re.findall(interval_regex, input_expr)
    remained_input_expr = re.sub(interval_regex, "", input_expr)
    interval_regex_2 = "(?<=\[\[).*?(?=\]\])"
    interval_patterns += re.findall(interval_regex_2, remained_input_expr)
    remained_input_expr = re.sub(interval_regex_2, "", remained_input_expr)
    case_patterns = re.sub("#+", "#", re.sub("[\]\[]", "", remained_input_expr)).strip("#").split("#")

    interval_patterns = interval_expr_to_unicode(interval_patterns)
    case_patterns = [string_to_unicode(case) for case in case_patterns]

    interval_pattern_string = "[%s]" % "".join(interval_patterns) if len(interval_patterns) > 0 else ""
    case_pattern_string = omit_blank_join("|", case_patterns)
    output_expr = omit_blank_join("|", [case_pattern_string, interval_pattern_string])

    return output_expr


def unicode_converter(input_expr):
    interval_regex = "\\\\u[a-zA-Z0-9]{4}\-\\\\u[a-zA-Z0-9]{4}"
    interval_patterns = re.findall(interval_regex, input_expr)
    remained_input_expr = re.sub(interval_regex, "", input_expr)
    interval_regex_2 = "(?<=\[).*?(?=\])"
    interval_patterns += re.findall(interval_regex_2, remained_input_expr)
    remained_input_expr = re.sub(interval_regex_2, "", remained_input_expr)
    case_patterns = re.sub("\|+", "|", re.sub("[\]\[]", "", remained_input_expr)).strip("|").split("|")

    interval_patterns = interval_unicode_to_char(interval_patterns)
    case_patterns = [unicode_to_string(case) for case in case_patterns]

    interval_pattern_string = "[%s]" % "".join(interval_patterns) if len(interval_patterns) > 0 else ""
    case_pattern_string = omit_blank_join("|", case_patterns)
    output_expr = omit_blank_join("|", [case_pattern_string, interval_pattern_string])

    return output_expr


def uu_merge(char_string):
    return expr_converter("[[%s]]" % char_string).strip("[").strip("]")


def uu_enum(unicode_string):
    return unicode_converter("[%s]" % unicode_string).strip("[").strip("]")


def unicode_decode(input):
    sss = "ɑ"
    '__'.join([i for i in unicodedata.normalize("NFKC", sss)])
    return input
