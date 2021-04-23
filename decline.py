import re
from typing import Optional, Pattern, Union, Dict, Callable, Match
from dataclasses import dataclass
import csv


@dataclass
class Declension:
    abs_sg: str
    con_sg: str
    gen_sg: str
    abs_pl: str
    con_pl: str
    gen_pl: str


letter_with_dagesh_lene = {
    "t": "T",
    "d": "D",
    "g": "G",
    "v": "b",
    "f": "p",
    "x": "k",
}

letter_lene = {
    "T": "t",
    "D": "d",
    "G": "g",
    "b": "v",
    "p": "f",
    "k": "x",
}

CON: Dict[int, Pattern[str]] = {
    2: re.compile(r"a(?=!.Á?$)"),
    3: re.compile(r"(.)a(.)e!(?=.Á?$)"),
    4: re.compile(r"[ea](.)$"),
    5: re.compile(r"(.)a(?=..!(.Á?)?$)"),
    6: re.compile(r"e!(.)Á?$"),
    7: re.compile(r"A!yI"),
    8: re.compile(r"o!(?=.Á?$)"),
    9: re.compile(r"[3á](.).(?=.$|..!.$)"),
    10: re.compile(r"a!wE"),
    11: re.compile(r"A!yI"),
    12: re.compile(r"(.)o!(.)i$"),
    13: re.compile(r"E!H$"),
    14: re.compile(r"(.)(I_|[e3])(.)a(?=.W!n$)"),
    15: re.compile(r"a(.)e!(?=.$)"),
    16: re.compile(r"a!(.)$"),
    17: re.compile(r"A(?=.$)"),
    18: re.compile(r"([oOAa])(.)$"),
    19: re.compile(r"(.)[ea](.)([iuWeA])!(.)Á?$"),
    20: re.compile(r"_(.)e!(.)Á?$"),
    21: re.compile(r"i!$"),
    22: re.compile(r"(.)([AEae])(?=.$)"),
    23: re.compile(r"[AEe](.)$"),
    24: re.compile(r"!(.)$"),
    25: re.compile(r"(.)[3á](.)i!$"),
    26: re.compile(r"(.)[ée](.)[eAE]!(.)$"),
    27: re.compile(r"á(.)e!(?=.Á?$)"),
    28: re.compile(r"([Eo])!(?=.$)"),
    29: re.compile(r"e(.)A!(.)$"),
    30: re.compile(r"([oAE])!(?=.$)"),
    31: re.compile(r"([ae])(?=.$)"),
    32: re.compile(r"[oAEae]!(.)[AE](.)$"),
    33: re.compile(r"o!(.)i$"),
    34: re.compile(r"a!(.)u$"),
    35: re.compile(r"o!(.)A(.)$"),
    36: re.compile(r"(?<=A)!(.)A(.)$"),
    37: re.compile(r"(.)[ea](.)(.)!(?=.Á?$)"),
    38: re.compile(r"(.)[ae](?=.$)"),
    42: re.compile(r"[Á!]"),
    43: re.compile(r"[UO](?=.$)"),
    44: re.compile(r"(.)([AIUEO])(.)[áéó]?(.)$"),
    45: re.compile(r"(.)A(?=.$)"),
    46: re.compile(r"(.)A!yI"),
    47: re.compile(r"i!$"),
    48: re.compile(r"[uoW](?=.$)"),
    49: re.compile(r"A(?=.$)"),
    50: re.compile(r"_(.)A(?=.$)"),
    51: re.compile(r"i$"),
    52: re.compile(r"3(.)i!$"),
    53: re.compile(r"[oiWOAI](?=N?.$)"),
    55: re.compile(r"[Ee]!(?=.$)"),
    63: re.compile(r"(.)([eaA])(?=.$)"),
    64: re.compile(r"([3áé])(.)[ae](?=.$)"),
    65: re.compile(r"[3á](.)[ae](.)(?=$)"),
    66: re.compile(r"I(?=.$)"),
    67: re.compile(r"O(.)(.)"),
    68: re.compile(r"_(.)a(?=.$)"),
    69: re.compile(r"a(?=.$)"),
}


def try_sub(
    index: int, repl: Union[str, Callable[[Match[str]], str]], word: str
) -> Optional[str]:
    regex = CON[index]
    if regex.search(word):
        return regex.sub(repl, word)
    return None


def add_dagesh(c: str) -> str:
    return letter_with_dagesh_lene.get(c, c)


def rm_dagesh(c: str) -> str:
    return letter_lene.get(c, c)


def is_gronit(c: str) -> bool:
    return c in "hRQj"


def is_hjR(c: str) -> bool:
    return c in "hjR"


def add_shwa_mobile(c: str, hataf: str = "á") -> str:
    return c + (hataf if is_gronit(c) else "3")


def make_con_sg_stem(abs_sg: str, suf_sg: str, con_sg: str) -> Optional[str]:
    if con_sg == "#1":
        return abs_sg
    elif con_sg == "#2":
        return try_sub(2, "A", abs_sg)
    elif con_sg == "#3":
        if suf_sg in ("E!H", "a!H", "e!H"):
            return try_sub(38, lambda m: add_shwa_mobile(m[1]), abs_sg)
        return try_sub(
            37,
            lambda m: add_shwa_mobile(m[1])
            + m[2]
            + ("A" if m[3] == "a" else m[3])
            + "!",
            abs_sg,
        )
    elif con_sg == "#3_A":
        return try_sub(3, lambda m: add_shwa_mobile(m[1]) + m[2] + "A!", abs_sg)
    elif con_sg == "#4":
        return try_sub(4, lambda m: ("A!" if is_hjR(m[1]) else "E!") + m[1], abs_sg)
    elif con_sg == "#5":
        return try_sub(5, lambda m: add_shwa_mobile(m[1]), abs_sg)
    elif con_sg == "#6":
        return try_sub(6, r"a!\1", abs_sg)
    elif con_sg == "#7":
        return try_sub(7, "i!", abs_sg)
    elif con_sg == "#8":
        return try_sub(8, "O!", abs_sg)
    elif con_sg in ("#9_E", "#9_I", "#9_A"):
        typ = con_sg[3]
        return try_sub(
            9, lambda m: typ + m[1] + ("á" if is_gronit(m[1]) else ""), abs_sg
        )
    elif con_sg == "#10":
        return abs_sg.replace("a!wE", "W!")
    elif con_sg == "#11":
        return abs_sg.replace("A!yI", "e!Y")
    elif con_sg == "#12":
        return try_sub(12, lambda m: add_shwa_mobile(m[1], "ó") + m[2] + "i!", abs_sg)
    elif con_sg == "#13":
        return try_sub(13, "i!", abs_sg)
    elif con_sg == "#14":
        return try_sub(
            14,
            lambda m: m[1]
            + ("E" if m[2] == "I_" and is_gronit(m[1]) else "I")
            + rm_dagesh(m[3]),
            abs_sg,
        )
    elif con_sg == "#15":
        return try_sub(15, r"E!\1E", abs_sg)
    elif con_sg == "#16":
        return try_sub(16, r"á\1i!", abs_sg)
    return con_sg


def make_gen_sg_stem(
    abs_sg: str, suf_sg: str, con_sg: str, gen_sg: str
) -> Optional[str]:
    cons = re.sub(r"[Á!]", "", con_sg)

    if gen_sg == "#1":
        if suf_sg == "E!H":
            return abs_sg
        return cons

    elif gen_sg == "#2":
        return try_sub(17, "a", cons)

    elif gen_sg.startswith("#3"):
        typ = gen_sg[3]
        return try_sub(32, lambda m: typ + m[1] + add_dagesh(m[2]), con_sg)

    elif gen_sg == "#4":
        return try_sub(
            18, lambda m: ("U_" if m[1] in "oO" else "A_") + add_dagesh(m[2]), cons
        )

    elif gen_sg == "#5":
        return try_sub(
            19,
            lambda m: add_shwa_mobile(m[1])
            + m[2]
            + ("a" if m[3] == "A" else m[3])
            + m[4],
            abs_sg,
        )

    elif gen_sg == "#6":
        if suf_sg in ("Et", "At"):
            return try_sub(30, lambda m: "O" if m[1] == "o" else "A", abs_sg)
        else:
            assert suf_sg in ("a!H_Et", "a!H_At")
            return try_sub(31, "A", abs_sg)

    elif gen_sg == "#7":
        return try_sub(20, r"\1\2", abs_sg)

    elif gen_sg == "#8":
        return try_sub(21, "I_y", con_sg)

    elif gen_sg == "#9":
        return try_sub(22, lambda m: add_shwa_mobile(m[1]), cons)

    elif gen_sg == "#10":
        return try_sub(23, lambda m: "I_" + add_dagesh(m[1]), cons)

    elif gen_sg == "#11":
        return (
            try_sub(33, r"O\1y", abs_sg)
            or try_sub(34, r"A\1w", abs_sg)
            or try_sub(35, r"O\1ó\2", abs_sg)
            or try_sub(36, r"\1á\2", abs_sg)
        )

    elif gen_sg == "#12":
        return try_sub(24, r"\1i", abs_sg)

    elif gen_sg == "#13":
        return try_sub(
            25,
            lambda m: m[1]
            + ("E" if is_gronit(m[1]) or is_gronit(m[2]) else "I")
            + m[2]
            + "y",
            abs_sg,
        )

    elif gen_sg == "#14":
        return try_sub(
            26, lambda m: add_shwa_mobile(m[1]) + m[2] + "I_" + add_dagesh(m[3]), abs_sg
        )

    elif gen_sg == "#15":
        return try_sub(27, r"A\1", abs_sg)

    elif gen_sg == "#16":
        return try_sub(28, lambda m: ("I" if m[1] in "E" else "U"), con_sg)

    elif gen_sg == "#17":
        return abs_sg + "ey"

    elif gen_sg == "#18":
        return try_sub(29, lambda m: "3" + m[1] + "A_" + add_dagesh(m[2]), abs_sg)

    elif gen_sg == "#19":
        return cons + "Q"

    return gen_sg


def make_abs_pl_stem(
    abs_pl: str, abs_sg: str, con_sg: str, gen_sg: str
) -> Optional[str]:
    if abs_pl == "#1":
        return gen_sg
    elif abs_pl == "#2":
        return CON[42].sub("", abs_sg)
    elif abs_pl == "#3":
        return try_sub(43, "W", gen_sg)
    elif abs_pl == "#4":
        return try_sub(
            44,
            lambda m: add_shwa_mobile(m[1], ("ó" if m[2] == "O" else "á"))
            + m[3]
            + "a"
            + rm_dagesh(m[4]),
            gen_sg,
        )
    elif abs_pl == "#5":
        return try_sub(45, lambda m: add_shwa_mobile(m[1]), gen_sg)
    elif abs_pl == "#6":
        return try_sub(46, lambda m: add_shwa_mobile(m[1]) + "ya", abs_sg)
    elif abs_pl == "#7":
        return try_sub(47, "aQ", con_sg)
    elif abs_pl == "#8":
        return try_sub(48, "3wa", gen_sg)
    elif abs_pl == "#9":
        return try_sub(49, "i", gen_sg)
    elif abs_pl == "#10":
        return try_sub(50, r"\1", gen_sg)
    elif abs_pl == "#11":
        return try_sub(51, "I_y", gen_sg)
    elif abs_pl == "#12":
        return try_sub(52, r"e\1", abs_sg)
    elif abs_pl == "#13":
        return try_sub(53, "a", gen_sg)
    elif abs_pl == "#15":
        return try_sub(55, "a", con_sg)
    else:
        return abs_pl


def make_con_pl_stem(con_pl: str, abs_pl: str, gen_sg: str) -> Optional[str]:
    if con_pl == "#1":
        return abs_pl
    elif con_pl == "#2":
        return gen_sg
    elif con_pl == "#3":
        return try_sub(63, lambda m: add_shwa_mobile(m[1]), abs_pl)
    elif con_pl == "#4":
        return try_sub(
            64,
            lambda m: ("E" if m[1] == "é" else "A")
            + m[2]
            + ("á" if is_gronit(m[2]) else ""),
            abs_pl,
        )
    elif con_pl == "#5":
        return try_sub(
            65,
            lambda m: "I"
            + m[1]
            + ("á" if is_gronit(m[1]) else ("3" if m[1] == m[2] else ""))
            + m[2],
            abs_pl,
        )
    elif con_pl == "#6":
        return try_sub(66, "i", gen_sg)
    elif con_pl == "#7":
        return try_sub(
            67,
            lambda m: "O" + m[1] + ("ó" if is_gronit(m[1]) else "") + rm_dagesh(m[2]),
            gen_sg,
        )
    elif con_pl == "#8":
        return try_sub(68, r"\1", abs_pl)
    elif con_pl == "#9":
        return try_sub(69, "3", abs_pl)
    else:
        return con_pl


SUF_SG_TO_SUF_CON_SG = {
    "e!H": "e!H",
    "E!H": "e!H",
    "a!H": "A!t",
    # "i!t": "i!t",
    # "u!t": "u!t",
    "-": "",
    "a!H_Et": "Et",
    "a!H_At": "At",
    # "Et": "Et",
    # "At": "At",
    # "A!Ny": "A!Ny",
}

SUF_SG_TO_SUF_GEN = {
    "e!H": "",
    "E!H": "",
    "a!H": "at",
    "i!t": "it",
    "u!t": "ut",
    "-": "",
    "a!H_Et": "T",
    "a!H_At": "T",
    "Et": "T",
    "At": "T",
    "A!Ny": "aQ",
}

SUF_SG_TO_AUX_PL = {
    "A!Ny": "aQ",
    "u!t": "U_y",
    "i!t": "I_y",
}

SUF_PL_TO_SUF_CON_PL = {
    "W!t": "W!t",
    "i!m": "e!Y",
    "A!yIm": "e!Y",
}


def decline(
    abs_sg: str,
    con_sg: str,
    gen_sg: str,
    abs_pl: str,
    con_pl: str,
    gen_pl: str,
    suf_sg: str,
    suf_pl: str,
) -> Optional[Declension]:
    if suf_sg == "a!H_Et" and is_hjR(abs_sg[-1]):
        suf_sg = "a!H_At"
    if suf_sg == "Et" and is_hjR(abs_sg[-1]):
        suf_sg = "At"

    abs_sg_suffix = ""
    if suf_sg in ("a!H_Et", "a!H_At"):
        abs_sg_suffix = "a!H"
    elif suf_sg != "-":
        abs_sg_suffix = suf_sg

    con_sg_stem = make_con_sg_stem(abs_sg=abs_sg, suf_sg=suf_sg, con_sg=con_sg)
    con_sg_suffix = SUF_SG_TO_SUF_CON_SG.get(suf_sg, suf_sg)
    if con_sg_stem is None:
        return None

    gen_sg_stem = make_gen_sg_stem(
        abs_sg=abs_sg, suf_sg=suf_sg, con_sg=con_sg_stem, gen_sg=gen_sg
    )
    gen_sg_suffix = SUF_SG_TO_SUF_GEN[suf_sg] + ("" if gen_sg_stem[-1] == "i" else "i")
    if gen_sg_stem is None:
        return None

    abs_pl_stem = make_abs_pl_stem(
        abs_pl=abs_pl, abs_sg=abs_sg, con_sg=con_sg_stem, gen_sg=gen_sg_stem
    )
    abs_pl_suffix = SUF_SG_TO_AUX_PL.get(suf_sg, "") + suf_pl
    if abs_pl_stem is None:
        return None

    con_pl_stem = make_con_pl_stem(
        con_pl=con_pl, abs_pl=abs_pl_stem, gen_sg=gen_sg_stem
    )
    con_pl_suffix = SUF_SG_TO_AUX_PL.get(suf_sg, "") + SUF_PL_TO_SUF_CON_PL[suf_pl]
    if con_pl_stem is None:
        return None

    gen_pl_stem = abs_pl_stem if gen_pl == "#1" else con_pl_stem
    gen_pl_suffix = (
        SUF_SG_TO_AUX_PL.get(suf_sg, "") + ("Wt" if suf_pl == "W!t" else "") + "Ay"
    )

    return Declension(
        abs_sg=abs_sg + abs_sg_suffix,
        con_sg=con_sg_stem + con_sg_suffix,
        gen_sg=gen_sg_stem + gen_sg_suffix,
        abs_pl=abs_pl_stem + abs_pl_suffix,
        con_pl=con_pl_stem + con_pl_suffix,
        gen_pl=gen_pl_stem + gen_pl_suffix,
    )


paradigm_parameters = {
    "b_sus": dict(con_sg="#1", gen_sg="#1", abs_pl="#1", con_pl="#1", gen_pl="#1"),
    "b_ets": dict(con_sg="#1", gen_sg="#1", abs_pl="#1", con_pl="#3", gen_pl="#1"),
    "b_simla": dict(con_sg="#1", gen_sg="#1", abs_pl="#4", con_pl="#2", gen_pl="#2"),
    "b_yalda": dict(con_sg="#1", gen_sg="#1", abs_pl="#4", con_pl="#4", gen_pl="#2"),
    "b_shuq": dict(con_sg="#1", gen_sg="#1", abs_pl="#8", con_pl="#2", gen_pl="#1"),
    "b_shen": dict(con_sg="#1", gen_sg="#10", abs_pl="#1", con_pl="#1", gen_pl="#1"),
    "b_baal": dict(con_sg="#1", gen_sg="#11", abs_pl="#4", con_pl="#2", gen_pl="#1"),
    "b_yaar": dict(con_sg="#1", gen_sg="#11", abs_pl="#4", con_pl="#2", gen_pl="#2"),
    "b_acu": dict(con_sg="#1", gen_sg="#11", abs_pl="#4", con_pl="#4", gen_pl="#1"),
    "b_kli": dict(con_sg="#1", gen_sg="#13", abs_pl="#12", con_pl="#3", gen_pl="#1"),
    "b_gdi": dict(con_sg="#1", gen_sg="#13", abs_pl="#4", con_pl="#1", gen_pl="#1"),
    "b_tsvi": dict(con_sg="#1", gen_sg="#13", abs_pl="#7", con_pl="#1", gen_pl="#1"),
    "b_emet": dict(con_sg="#1", gen_sg="#14", abs_pl="#1", con_pl="#1", gen_pl="#1"),
    "b_macave": dict(con_sg="#1", gen_sg="#15", abs_pl="#1", con_pl="#1", gen_pl="#1"),
    "b_gveret": dict(con_sg="#1", gen_sg="#16", abs_pl="#13", con_pl="#6", gen_pl="#2"),
    "b_maskoret": dict(
        con_sg="#1", gen_sg="#16", abs_pl="#3", con_pl="#1", gen_pl="#1"
    ),
    "b_se": dict(con_sg="#1", gen_sg="#17", abs_pl="#1", con_pl="#3", gen_pl="#1"),
    "b_memad": dict(con_sg="#1", gen_sg="#18", abs_pl="#1", con_pl="#1", gen_pl="#1"),
    "b_par": dict(con_sg="#1", gen_sg="#2", abs_pl="#1", con_pl="#1", gen_pl="#1"),
    "b_emtsa": dict(con_sg="#1", gen_sg="#2", abs_pl="#1", con_pl="#3", gen_pl="#1"),
    "b_qarqa": dict(con_sg="#1", gen_sg="#2", abs_pl="#1", con_pl="#3", gen_pl="#2"),
    "b_regel": dict(con_sg="#1", gen_sg="#3_A", abs_pl="#1", con_pl="#1", gen_pl="#1"),
    "b_yerac": dict(con_sg="#1", gen_sg="#3_A", abs_pl="#4", con_pl="#2", gen_pl="#1"),
    "b_erets": dict(con_sg="#1", gen_sg="#3_A", abs_pl="#4", con_pl="#2", gen_pl="#2"),
    "b_derex": dict(con_sg="#1", gen_sg="#3_A", abs_pl="#4", con_pl="#4", gen_pl="#1"),
    "b_delet": dict(con_sg="#1", gen_sg="#3_A", abs_pl="#4", con_pl="#4", gen_pl="#2"),
    "b_nexed": dict(con_sg="#1", gen_sg="#3_E", abs_pl="#4", con_pl="#1", gen_pl="#1"),
    "b_celeq": dict(con_sg="#1", gen_sg="#3_E", abs_pl="#4", con_pl="#2", gen_pl="#1"),
    "b_berex": dict(con_sg="#1", gen_sg="#3_I", abs_pl="#1", con_pl="#1", gen_pl="#1"),
    "b_sefer": dict(con_sg="#1", gen_sg="#3_I", abs_pl="#4", con_pl="#2", gen_pl="#1"),
    "b_shemesh": dict(
        con_sg="#1", gen_sg="#3_I", abs_pl="#4", con_pl="#2", gen_pl="#2"
    ),
    "b_kotel": dict(con_sg="#1", gen_sg="#3_O", abs_pl="#4", con_pl="#2", gen_pl="#1"),
    "b_orac": dict(con_sg="#1", gen_sg="#3_O", abs_pl="#4", con_pl="#2", gen_pl="#2"),
    "b_rocav": dict(con_sg="#1", gen_sg="#3_O", abs_pl="#4", con_pl="#7", gen_pl="#1"),
    "b_qomets": dict(con_sg="#1", gen_sg="#3_U", abs_pl="#4", con_pl="#2", gen_pl="#1"),
    "b_tof": dict(con_sg="#1", gen_sg="#4", abs_pl="#1", con_pl="#1", gen_pl="#1"),
    "b_?1": dict(
        con_sg="#1", gen_sg="#4", abs_pl="mAjámA_D", con_pl="#1", gen_pl="#1"
    ),  # FIXME
    "b_ezor": dict(con_sg="#1", gen_sg="#5", abs_pl="#1", con_pl="#1", gen_pl="#1"),
    "b_piqacat": dict(con_sg="#1", gen_sg="#6", abs_pl="#10", con_pl="#1", gen_pl="#1"),
    "b_koteret": dict(con_sg="#1", gen_sg="#6", abs_pl="#13", con_pl="#3", gen_pl="#2"),
    "b_atseret": dict(con_sg="#1", gen_sg="#6", abs_pl="#13", con_pl="#4", gen_pl="#2"),
    "b_mishqolet": dict(
        con_sg="#1", gen_sg="#6", abs_pl="#3", con_pl="#1", gen_pl="#1"
    ),
    "b_poelet": dict(con_sg="#1", gen_sg="#6", abs_pl="#5", con_pl="#1", gen_pl="#1"),
    "b_maskelet": dict(con_sg="#1", gen_sg="#6", abs_pl="#9", con_pl="#1", gen_pl="#1"),
    "b_maqel": dict(con_sg="#1", gen_sg="#7", abs_pl="#1", con_pl="#1", gen_pl="#1"),
    "b_i": dict(con_sg="#1", gen_sg="#8", abs_pl="#1", con_pl="#1", gen_pl="#1"),
    "b_shomer": dict(con_sg="#1", gen_sg="#9", abs_pl="#1", con_pl="#1", gen_pl="#1"),
    "b_qodqod": dict(
        con_sg="#1", gen_sg="qOdqód", abs_pl="#1", con_pl="#1", gen_pl="#1"
    ),  # FIXME
    "b_mawet": dict(con_sg="#10", gen_sg="#1", abs_pl="#1", con_pl="#1", gen_pl="#1"),
    "b_zayit": dict(con_sg="#11", gen_sg="#1", abs_pl="#1", con_pl="#1", gen_pl="#1"),
    "b_tayish": dict(con_sg="#11", gen_sg="#1", abs_pl="#6", con_pl="#2", gen_pl="#1"),
    "b_ayin": dict(con_sg="#11", gen_sg="#1", abs_pl="#6", con_pl="#2", gen_pl="#2"),
    "b_qoshi": dict(con_sg="#12", gen_sg="#11", abs_pl="#4", con_pl="#1", gen_pl="#1"),
    "b_?2": dict(
        con_sg="#12", gen_sg="#11", abs_pl="#7", con_pl="#1", gen_pl="#1"
    ),  # FIXME
    "b_pe": dict(con_sg="#13", gen_sg="#1", abs_pl="#11", con_pl="#1", gen_pl="#1"),
    "b_zikaron": dict(con_sg="#14", gen_sg="#1", abs_pl="#1", con_pl="#1", gen_pl="#1"),
    "b_gader": dict(con_sg="#15", gen_sg="#5", abs_pl="#1", con_pl="#5", gen_pl="#1"),
    "b_av": dict(con_sg="#16", gen_sg="#12", abs_pl="#2", con_pl="#3", gen_pl="#2"),
    "b_ac": dict(
        con_sg="#16", gen_sg="#12", abs_pl="QAj", con_pl="#3", gen_pl="#1"
    ),  # FIXME
    "b_dat": dict(con_sg="#2", gen_sg="#2", abs_pl="#1", con_pl="#1", gen_pl="#1"),
    "b_binyan": dict(con_sg="#2", gen_sg="#2", abs_pl="#1", con_pl="#3", gen_pl="#1"),
    "b_kikar": dict(con_sg="#2", gen_sg="#2", abs_pl="#1", con_pl="#3", gen_pl="#2"),
    "b_maacal": dict(con_sg="#2", gen_sg="#2", abs_pl="#1", con_pl="#4", gen_pl="#1"),
    "b_masa": dict(con_sg="#2", gen_sg="#2", abs_pl="#1", con_pl="#8", gen_pl="#1"),
    "b_?3": dict(
        con_sg="#2", gen_sg="#2", abs_pl="#1", con_pl="maROmd", gen_pl="#1"
    ),  # FIXME
    "b_aqrav": dict(con_sg="#2", gen_sg="#4", abs_pl="#1", con_pl="#1", gen_pl="#1"),
    "b_paqid": dict(con_sg="#3", gen_sg="#1", abs_pl="#1", con_pl="#1", gen_pl="#1"),
    "b_avel": dict(con_sg="#3", gen_sg="#1", abs_pl="#1", con_pl="#1", gen_pl="#1"),
    "b_qane": dict(con_sg="#3", gen_sg="#1", abs_pl="#1", con_pl="#3", gen_pl="#1"),
    "b_sade": dict(con_sg="#3", gen_sg="#1", abs_pl="#1", con_pl="#3", gen_pl="#2"),
    "b_caver": dict(con_sg="#3", gen_sg="#1", abs_pl="#1", con_pl="#4", gen_pl="#1"),
    "b_aqev": dict(con_sg="#3", gen_sg="#1", abs_pl="#1", con_pl="#5", gen_pl="#1"),
    "b_shana": dict(con_sg="#3", gen_sg="#1", abs_pl="#2", con_pl="#2", gen_pl="#2"),
    "b_saef": dict(con_sg="#3", gen_sg="#10", abs_pl="#1", con_pl="#1", gen_pl="#1"),
    "b_kanaf": dict(con_sg="#3", gen_sg="#2", abs_pl="#1", con_pl="#4", gen_pl="#1"),
    "b_zanav": dict(con_sg="#3", gen_sg="#2", abs_pl="#1", con_pl="#4", gen_pl="#2"),
    "b_davar": dict(con_sg="#3", gen_sg="#2", abs_pl="#1", con_pl="#5", gen_pl="#1"),
    "b_levav": dict(con_sg="#3", gen_sg="#2", abs_pl="#1", con_pl="#5", gen_pl="#2"),
    "b_adom": dict(con_sg="#3", gen_sg="#4", abs_pl="#1", con_pl="#1", gen_pl="#1"),
    "b_catser": dict(con_sg="#3_A", gen_sg="#5", abs_pl="#1", con_pl="#4", gen_pl="#2"),
    "b_zaqen": dict(con_sg="#3_A", gen_sg="#5", abs_pl="#1", con_pl="#5", gen_pl="#1"),
    "b_shxena": dict(con_sg="#4", gen_sg="#1", abs_pl="#2", con_pl="#1", gen_pl="#1"),
    "b_milcama": dict(con_sg="#4", gen_sg="#6", abs_pl="#2", con_pl="#3", gen_pl="#2"),
    "b_atara": dict(con_sg="#4", gen_sg="#6", abs_pl="#2", con_pl="#4", gen_pl="#2"),
    "b_ayala": dict(con_sg="#4", gen_sg="#6", abs_pl="#2", con_pl="#8", gen_pl="#2"),
    "b_yoleda": dict(con_sg="#4", gen_sg="#6", abs_pl="#5", con_pl="#1", gen_pl="#1"),
    "b_tsava": dict(con_sg="#5", gen_sg="#1", abs_pl="#1", con_pl="#5", gen_pl="#2"),
    "b_tsali": dict(con_sg="#5", gen_sg="#8", abs_pl="#1", con_pl="#1", gen_pl="#1"),
    "b_mizbeac": dict(con_sg="#6", gen_sg="#9", abs_pl="#1", con_pl="#1", gen_pl="#1"),
    "b_ayir": dict(con_sg="#7", gen_sg="#1", abs_pl="#6", con_pl="#2", gen_pl="#1"),
    "b_coq": dict(con_sg="#8", gen_sg="#4", abs_pl="#1", con_pl="#1", gen_pl="#1"),
    "b_adama": dict(con_sg="#9_A", gen_sg="#1", abs_pl="#2", con_pl="#2", gen_pl="#2"),
    "b_arafel": dict(
        con_sg="#9_A", gen_sg="#10", abs_pl="#1", con_pl="#1", gen_pl="#1"
    ),
    "b_agala": dict(con_sg="#9_E", gen_sg="#1", abs_pl="#2", con_pl="#2", gen_pl="#2"),
    "b_nedava": dict(con_sg="#9_I", gen_sg="#1", abs_pl="#2", con_pl="#2", gen_pl="#2"),
    "b_tslatsal": dict(
        con_sg="#9_I", gen_sg="#4", abs_pl="#1", con_pl="#1", gen_pl="#1"
    ),
    "b_?4": dict(
        con_sg="SWne!Nt", gen_sg="#1", abs_pl="SWn3Q", con_pl="#1", gen_pl="#1"
    ),  # FIXME
    "b_yom": dict(con_sg="#1", gen_sg="#1", abs_pl="#13", con_pl="#9", gen_pl="#1"),
    "b_ir": dict(con_sg="#1", gen_sg="#1", abs_pl="#13", con_pl="#1", gen_pl="#1"),
    "b_ish": dict(con_sg="#1", gen_sg="#1", abs_pl="Qánac", con_pl="#4", gen_pl="#1"),
    "b_ot_neqeva": dict(
        con_sg="#1", gen_sg="#1", abs_pl="QWtI_y", con_pl="#1", gen_pl="#1"
    ),
    "b_bat": dict(con_sg="#1", gen_sg="#10", abs_pl="ban", con_pl="#9", gen_pl="#2"),
    "b_isha": dict(
        con_sg="Qe!cEt", gen_sg="QIcT", abs_pl="nac", con_pl="#9", gen_pl="#1"
    ),
    "b_acot": dict(
        con_sg="#3", gen_sg="#1", abs_pl="Qácay", con_pl="QAcy", gen_pl="#2"
    ),
    "b_bayit": dict(con_sg="#11", gen_sg="#1", abs_pl="ba_T", con_pl="#1", gen_pl="#1"),
    "b_ben": dict(con_sg="bE!n", gen_sg="#9", abs_pl="#15", con_pl="#2", gen_pl="#1"),
    "b_shem": dict(con_sg="#1", gen_sg="#9", abs_pl="#2", con_pl="#2", gen_pl="#2"),
    "b_dyo": dict(con_sg="#1", gen_sg="#19", abs_pl="#1", con_pl="#1", gen_pl="#1"),
    "b_tsel": dict(con_sg="#1", gen_sg="#10", abs_pl="Z3lal", con_pl="#5", gen_pl="#1"),
    "b_matoq": dict(con_sg="#5", gen_sg="m3tuq", abs_pl="#1", con_pl="#1", gen_pl="#1"),
    "b_tsipor": dict(
        con_sg="#1", gen_sg="#1", abs_pl="ZI_pór", con_pl="#1", gen_pl="#1"
    ),
    "b_ama": dict(con_sg="#3", gen_sg="#1", abs_pl="Qámah", con_pl="#4", gen_pl="#2"),
    "b_em": dict(
        con_sg="#1", gen_sg="#10", abs_pl="QI_mah", con_pl="QI_m3h", gen_pl="#2"
    ),
    "b_braxa": dict(
        con_sg="bIrk", gen_sg="bIrx", abs_pl="#2", con_pl="#2", gen_pl="#2"
    ),
    "b_lavi": dict(con_sg="#3", gen_sg="#1", abs_pl="#13", con_pl="#1", gen_pl="#1"),
    "b_tale": dict(con_sg="#3", gen_sg="#1", abs_pl="73laQ", con_pl="#1", gen_pl="#1"),
}

# Vs_yom Vs_bat Vs_ot_neqeva Vs_ish Vs_isha Vs_ir(/s_rosh) Vs_acot Vs_bayit Vs_ben Vs_shem
# Vs_ama Vs_em Vs_tsel Vs_dyo Vs_tsipor Vs_matoq
# Xs_snai(43*) s_ktav? Vs_tale Xs_esh?(171*) Vs_lavi
# Xs_tavla Vs_braxa Xs_arye(use b_simla) s_qatse(~qtsawot)
# s_tolaat? s_kneset? s_gawen? s_mayim? s_gay

# "b_qatse": dict(con_sg="q3Z", gen_sg="?", abs_pl="q3Zaw", con_pl="q3Z", gen_pl="?"),  # FIXME
# qatse,221*,qaZE!H-qaZe!H-?-q3ZawW!t-q3ZW!t-q3ZawWtAy,qaZ,#1,#1,q3Zaw,q3Z,#1,FALSE,E!H,W!t,

SINGULAR_SUFFIX = ["e!H", "a!H", "E!H", "Et", "At", "i!t", "u!t", "A!Ny"]


def decline_by_paradigm(
    paradigm_id: str, word: str, has_suf: bool, suf_pl: str
) -> Optional[Declension]:
    if paradigm_id.startswith("b_"):
        if has_suf:
            suf_sg = next(s for s in SINGULAR_SUFFIX if word.endswith(s))
            if suf_sg == "At":
                suf_sg = "Et"
            abs_sg = word[: -len(suf_sg)]
            if paradigm_id in [
                "b_shxena",
                "b_milcama",
                "b_atara",
                "b_ayala",
                "b_yoleda",
            ]:
                suf_sg = "a!H_Et"
        else:
            suf_sg = "-"
            abs_sg = word
        return decline(
            abs_sg=abs_sg,
            suf_sg=suf_sg,
            suf_pl=suf_pl,
            **paradigm_parameters[paradigm_id]
        )
    else:
        if paradigm_id in ("f_atom", "f_banana", "f_mango", "f_stati"):
            con_sg = word
            base_pl = word
            if word.endswith("aH"):
                con_sg = word[:-2] + "At"
                base_pl = word[:-2]
            elif re.match(r"[Wu]!?$", word):
                base_pl = con_sg + "Q"
            elif word.endswith("i"):
                base_pl = con_sg[:1] + "I_y"
            return Declension(
                abs_sg=word,
                con_sg=con_sg,
                gen_sg="",
                abs_pl=base_pl + suf_pl.replace("!", ""),
                con_pl=base_pl.replace("!", "") + "e!Y"
                if suf_pl == "im"
                else base_pl + suf_pl,
                gen_pl="",
            )
        elif paradigm_id == "f_universita":
            return Declension(
                abs_sg=word,
                con_sg=word[:-2] + "At",
                gen_sg="",
                abs_pl=word.replace("!", "") + suf_pl,
                con_pl=word.replace("!", "") + suf_pl,
                gen_pl="",
            )
        elif paradigm_id == "f_meter":
            return Declension(
                abs_sg=word,
                con_sg=word,
                gen_sg="",
                abs_pl=word[:-2] + word[-1] + "im",
                con_pl=word[:-2].replace("!", "") + word[-1] + "e!Y",
                gen_pl="",
            )
        elif paradigm_id == "f_telefon":
            return Declension(
                abs_sg=word,
                con_sg=word,
                gen_sg="",
                abs_pl=re.sub(
                    r"([aiueoAIUEOW])(?=[^aiueoAIUEOW]*$)",
                    r"\1!",
                    word.replace("!", ""),
                )
                + suf_pl,
                con_pl=word.replace("!", "") + "e!Y",
                gen_pl="",
            )
        elif paradigm_id == "f_geto":
            return Declension(
                abs_sg=word,
                con_sg=word,
                gen_sg="",
                abs_pl=word[:-1].replace("!", "") + suf_pl,
                con_pl=word[:-1].replace("!", "")
                + ("e!Y" if suf_pl == "im" else suf_pl),
                gen_pl="",
            )
        else:
            assert False
