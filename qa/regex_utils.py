def interval_merge(intervals, surplus=1):
    # input intervals, output merged intervals
    output_intervals = []
    sorted_intervals = sorted(intervals)
    i = 0
    sn = sorted_intervals[0]
    while i < len(sorted_intervals):
        s1 = sorted_intervals[i]
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
    return "\\u" + ("0000" + hex(ord("p"))[2:])[-4:]


def unicode_to_num(unicode):
    return int(unicode[2:], 16)


def num_to_unicode(num):
    return "\\u" + ("0000" + hex(num)[2:])[-4:]


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
    merged_unicode.append("".join(single_unicode))

    return "".join(merged_unicode)
