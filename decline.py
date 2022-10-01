from __future__ import annotations
import enum
import re
from typing import Literal, Optional, Callable
from dataclasses import dataclass


@dataclass
class Paradigm:
    con_sg: str | REConSG | Literal[0]
    gen_sg: str | REGenSG | Literal[0]
    abs_pl: str | REAbsPL | Literal[0]
    con_pl: str | REConPL | Literal[1, 2]
    gen_pl: Literal[1, 2]


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


class TrySubMixin:
    value: tuple[re.Pattern, str | Callable[[re.Match], str]]

    def try_sub(self, word: str) -> str | None:
        if self.value[0].search(word):
            return self.value[0].sub(self.value[1], word)
        return None


class REConSG(TrySubMixin, enum.Enum):
    C2 = (re.compile(r"a(?=!.Á?$)"), "A")
    C3 = (
        re.compile(r"(.)[ea](.)(.)!(?=.Á?$)"),
        lambda m: add_shwa_mobile(m[1]) + m[2] + ("A" if m[3] == "a" else m[3]) + "!",
    )
    C3_A = (
        re.compile(r"(.)a(.)e!(?=.Á?$)"),
        lambda m: add_shwa_mobile(m[1]) + m[2] + "A!",
    )
    C4 = (re.compile(r"[ea](.)$"), lambda m: ("A!" if is_hjR(m[1]) else "E!") + m[1])
    C5 = (re.compile(r"(.)a(?=..!(.Á?)?$)"), lambda m: add_shwa_mobile(m[1]))
    C6 = (re.compile(r"e!(.)Á?$"), r"a!\1")
    C7 = (re.compile(r"A!yI"), "i!")
    C8 = (re.compile(r"o!(?=.Á?$)"), "O!")
    C9_E = (
        re.compile(r"[3á](.).(?=.$|..!.$)"),
        lambda m: "E" + m[1] + ("á" if is_gronit(m[1]) else ""),
    )
    C9_I = (
        re.compile(r"[3á](.).(?=.$|..!.$)"),
        lambda m: "I" + m[1] + ("á" if is_gronit(m[1]) else ""),
    )
    C9_A = (
        re.compile(r"[3á](.).(?=.$|..!.$)"),
        lambda m: "A" + m[1] + ("á" if is_gronit(m[1]) else ""),
    )
    C10 = (re.compile(r"a!wE"), "a!wE")
    C11 = (re.compile(r"A!yI"), "A!yI")
    C12 = (
        re.compile(r"(.)o!(.)i$"),
        lambda m: add_shwa_mobile(m[1], "ó") + m[2] + "i!",
    )
    C13 = (re.compile(r"E!H$"), "i!")
    C14 = (
        re.compile(r"(.)(I_|[e3])(.)a(?=.W!n$)"),
        lambda m: m[1]
        + ("E" if m[2] == "I_" and is_gronit(m[1]) else "I")
        + rm_dagesh(m[3]),
    )
    C15 = (re.compile(r"a(.)e!(?=.$)"), r"E!\1E")
    C16 = (re.compile(r"a!(.)$"), r"á\1i!")
    C38 = (re.compile(r"(.)[ae](?=.$)"), lambda m: add_shwa_mobile(m[1]))


def make_con_sg_stem(
    abs_sg: str, suf_sg: str, con_sg: str | REConSG | Literal[0]
) -> Optional[str]:
    if isinstance(con_sg, str):
        return con_sg
    elif con_sg == 0:
        return abs_sg
    elif con_sg is REConSG.C3 and suf_sg in ("E!H", "a!H", "e!H"):
        return REConSG.C38.try_sub(abs_sg)
    else:
        return con_sg.try_sub(abs_sg)


class REGenSG(TrySubMixin, enum.Enum):
    C2 = (re.compile(r"A(?=.$)"), "a")
    C3_A = (
        re.compile(r"[oAEae]!(.)[AE](.)$"),
        lambda m: "A" + m[1] + add_dagesh(m[2]),
    )
    C3_I = (
        re.compile(r"[oAEae]!(.)[AE](.)$"),
        lambda m: "I" + m[1] + add_dagesh(m[2]),
    )
    C3_U = (
        re.compile(r"[oAEae]!(.)[AE](.)$"),
        lambda m: "U" + m[1] + add_dagesh(m[2]),
    )
    C3_E = (
        re.compile(r"[oAEae]!(.)[AE](.)$"),
        lambda m: "E" + m[1] + add_dagesh(m[2]),
    )
    C3_O = (
        re.compile(r"[oAEae]!(.)[AE](.)$"),
        lambda m: "O" + m[1] + add_dagesh(m[2]),
    )
    C4 = (
        re.compile(r"([oOAa])(.)$"),
        lambda m: ("U_" if m[1] in "oO" else "A_") + add_dagesh(m[2]),
    )
    C5 = (
        re.compile(r"(.)[ea](.)([iuWeA])!(.)Á?$"),
        lambda m: add_shwa_mobile(m[1]) + m[2] + ("a" if m[3] == "A" else m[3]) + m[4],
    )
    C6 = (re.compile(r"(.)a(..)!(?=.$)"), lambda m: add_shwa_mobile(m[1]) + m[2])
    C7 = (re.compile(r"_(.)e!(.)Á?$"), r"\1\2")
    C8 = (re.compile(r"i!$"), "I_y")
    C9 = (re.compile(r"(.)([AEae])(?=.$)"), lambda m: add_shwa_mobile(m[1]))
    C10 = (re.compile(r"[AEe](.)$"), lambda m: "I_" + add_dagesh(m[1]))
    C12 = (re.compile(r"!(.)$"), r"\1i")
    C13 = (
        re.compile(r"(.)[3á](.)i!$"),
        lambda m: m[1]
        + ("E" if is_gronit(m[1]) or is_gronit(m[2]) else "I")
        + m[2]
        + "y",
    )
    C14 = (
        re.compile(r"(.)[ée](.)[eAE]!(.)$"),
        lambda m: add_shwa_mobile(m[1]) + m[2] + "I_" + add_dagesh(m[3]),
    )
    C15 = (re.compile(r"á(.)e!(?=.Á?$)"), r"A\1")
    C16 = (re.compile(r"([Eo])!(?=.$)"), lambda m: ("I" if m[1] in "E" else "U"))
    C17 = (re.compile(r"$"), "ey")
    C18 = (re.compile(r"e(.)A!(.)$"), lambda m: "3" + m[1] + "A_" + add_dagesh(m[2]))
    C19 = (re.compile(r"$"), "Q")
    C30 = (re.compile(r"([oAE])!(?=.$)"), lambda m: "O" if m[1] == "o" else "A")
    C31 = (re.compile(r"([ae])(?=.$)"), "A")
    C33 = (re.compile(r"o!(.)i$"), r"O\1y")
    C34 = (re.compile(r"a!(.)u$"), r"A\1w")
    C35 = (re.compile(r"o!(.)A(.)$"), r"O\1ó\2")
    C36 = (re.compile(r"(?<=A)!(.)A(.)$"), r"\1á\2")


def make_gen_sg_stem(
    abs_sg: str,
    suf_sg: str,
    con_sg: str,
    gen_sg: str | Literal[0] | REGenSG,
) -> Optional[str]:
    cons = re.sub(r"[Á!]", "", con_sg)

    if gen_sg == 0:
        if suf_sg == "E!H":
            return abs_sg
        return cons
    elif isinstance(gen_sg, str):
        return gen_sg
    elif gen_sg in [REGenSG.C2, REGenSG.C4, REGenSG.C9, REGenSG.C10, REGenSG.C19]:
        return gen_sg.try_sub(cons)
    elif gen_sg in [REGenSG.C8, REGenSG.C16]:
        return gen_sg.try_sub(con_sg)
    elif gen_sg is REGenSG.C30 and suf_sg in ("a!H_Et", "a!H_At"):
        return REGenSG.C31.try_sub(abs_sg)
    else:
        return gen_sg.try_sub(abs_sg)


class REAbsPL(TrySubMixin, enum.Enum):
    C42 = (re.compile(r"[Á!]?"), "")
    C43 = (re.compile(r"[UO](?=.$)"), "W")
    C44 = (
        re.compile(r"(.)([AIUEO])(.)[áéó]?(.)$"),
        lambda m: add_shwa_mobile(m[1], ("ó" if m[2] == "O" else "á"))
        + m[3]
        + "a"
        + rm_dagesh(m[4]),
    )
    C45 = (re.compile(r"(.)[Ae](?=.$)"), lambda m: add_shwa_mobile(m[1]))
    C46 = (re.compile(r"(.)A!yI"), lambda m: add_shwa_mobile(m[1]) + "ya")
    C47 = (re.compile(r"i!$"), "aQ")
    C48 = (re.compile(r"[uoW](?=.$)"), "3wa")
    C49 = (re.compile(r"A(?=.$)"), "i")
    C50 = (re.compile(r"_(.)A(?=.$)"), r"\1")
    C51 = (re.compile(r"i$"), "I_y")
    C52 = (re.compile(r"3(.)i!$"), r"e\1")
    C53 = (re.compile(r"[oiWOAI](?=Q?.$)"), "a")
    C55 = (re.compile(r"[Ee]!(?=.$)"), "a")


def make_abs_pl_stem(
    abs_pl: REAbsPL | str | Literal[0], abs_sg: str, con_sg: str, gen_sg: str
) -> Optional[str]:
    if abs_pl == 0:
        return gen_sg
    elif isinstance(abs_pl, str):
        return abs_pl
    elif abs_pl in [REAbsPL.C42, REAbsPL.C46, REAbsPL.C52]:
        return abs_pl.try_sub(abs_sg)
    elif abs_pl in [REAbsPL.C47, REAbsPL.C55]:
        return abs_pl.try_sub(con_sg)
    else:
        return abs_pl.try_sub(gen_sg)


class REConPL(TrySubMixin, enum.Enum):
    C63 = (re.compile(r"(.)([eaA])(?=.$)"), lambda m: add_shwa_mobile(m[1]))
    C64 = (
        re.compile(r"([3áé])(.)[ae](?=.$)"),
        lambda m: ("E" if m[1] == "é" else "A")
        + m[2]
        + ("á" if is_gronit(m[2]) else ""),
    )
    C65 = (
        re.compile(r"[3á](.)[ae](.)(?=$)"),
        lambda m: "I"
        + m[1]
        + ("á" if is_gronit(m[1]) else ("3" if m[1] == m[2] else ""))
        + m[2],
    )
    C66 = (re.compile(r"I(?=.$)"), "i")
    C67 = (
        re.compile(r"O(.)(.)"),
        lambda m: "O" + m[1] + ("ó" if is_gronit(m[1]) else "") + rm_dagesh(m[2]),
    )
    C68 = (re.compile(r"_(.)a(?=.$)"), r"\1")
    C69 = (re.compile(r"a(?=.$)"), "3")


def make_con_pl_stem(
    con_pl: str | Literal[1, 2] | REConPL, abs_pl: str, gen_sg: str
) -> Optional[str]:
    if isinstance(con_pl, str):
        return con_pl
    elif con_pl == 1:
        return abs_pl
    elif con_pl == 2:
        return gen_sg
    elif con_pl in [REConPL.C66, REConPL.C67]:
        return con_pl.try_sub(gen_sg)
    else:
        return con_pl.try_sub(abs_pl)


SUF_SG_TO_SUF_CON_SG = {
    "e!H": "e!H",
    "E!H": "e!H",
    "a!H": "A!t",
    "-": "",
    "a!H_Et": "Et",
    "a!H_At": "At",
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
    "A!Qy": "aQ",
}

SUF_SG_TO_AUX_PL = {
    "A!Qy": "aQ",
    "u!t": "U_y",
    "i!t": "I_y",
}

SUF_PL_TO_SUF_CON_PL = {
    "W!t": "W!t",
    "i!m": "e!Y",
    "A!yIm": "e!Y",
    "aQW!t": "aQW!t",
}


def decline(
    abs_sg: str,
    suf_sg: str,
    suf_pl: str,
    paradigm: Paradigm,
    throw: bool = False
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

    con_sg_stem = make_con_sg_stem(abs_sg=abs_sg, suf_sg=suf_sg, con_sg=paradigm.con_sg)
    con_sg_suffix = SUF_SG_TO_SUF_CON_SG.get(suf_sg, suf_sg)
    if con_sg_stem is None:
        assert not throw
        return None

    gen_sg_stem = make_gen_sg_stem(
        abs_sg=abs_sg, suf_sg=suf_sg, con_sg=con_sg_stem, gen_sg=paradigm.gen_sg
    )
    if gen_sg_stem is None:
        assert not throw
        return None
    gen_sg_suffix = SUF_SG_TO_SUF_GEN[suf_sg] + ("" if gen_sg_stem[-1] == "i" else "i")

    abs_pl_stem = make_abs_pl_stem(
        abs_pl=paradigm.abs_pl, abs_sg=abs_sg, con_sg=con_sg_stem, gen_sg=gen_sg_stem
    )
    abs_pl_suffix = SUF_SG_TO_AUX_PL.get(suf_sg, "") + suf_pl
    if abs_pl_stem is None:
        assert not throw
        return None

    con_pl_stem = make_con_pl_stem(
        con_pl=paradigm.con_pl, abs_pl=abs_pl_stem, gen_sg=gen_sg_stem
    )
    con_pl_suffix = SUF_SG_TO_AUX_PL.get(suf_sg, "") + SUF_PL_TO_SUF_CON_PL[suf_pl]
    if con_pl_stem is None:
        assert not throw
        return None

    gen_pl_stem = abs_pl_stem if paradigm.gen_pl == 1 else con_pl_stem
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
    "b_sus": Paradigm(con_sg=0, gen_sg=0, abs_pl=0, con_pl=1, gen_pl=1),
    "b_ets": Paradigm(con_sg=0, gen_sg=0, abs_pl=0, con_pl=REConPL.C63, gen_pl=1),
    "b_simla": Paradigm(con_sg=0, gen_sg=0, abs_pl=REAbsPL.C44, con_pl=2, gen_pl=2),
    "b_yalda": Paradigm(
        con_sg=0, gen_sg=0, abs_pl=REAbsPL.C44, con_pl=REConPL.C64, gen_pl=2
    ),
    "b_shuq": Paradigm(con_sg=0, gen_sg=0, abs_pl=REAbsPL.C48, con_pl=2, gen_pl=1),
    "b_shen": Paradigm(con_sg=0, gen_sg=REGenSG.C10, abs_pl=0, con_pl=1, gen_pl=1),
    "b_baal": Paradigm(
        con_sg=0, gen_sg=REGenSG.C36, abs_pl=REAbsPL.C44, con_pl=2, gen_pl=1
    ),
    "b_yaar": Paradigm(
        con_sg=0, gen_sg=REGenSG.C36, abs_pl=REAbsPL.C44, con_pl=2, gen_pl=2
    ),
    "b_acu": Paradigm(
        con_sg=0, gen_sg=REGenSG.C34, abs_pl=REAbsPL.C44, con_pl=REConPL.C64, gen_pl=1
    ),
    "b_kli": Paradigm(
        con_sg=0, gen_sg=REGenSG.C13, abs_pl=REAbsPL.C52, con_pl=REConPL.C63, gen_pl=1
    ),
    "b_gdi": Paradigm(
        con_sg=0, gen_sg=REGenSG.C13, abs_pl=REAbsPL.C44, con_pl=1, gen_pl=1
    ),
    "b_tsvi": Paradigm(
        con_sg=0, gen_sg=REGenSG.C13, abs_pl=REAbsPL.C47, con_pl=1, gen_pl=1
    ),
    "b_emet": Paradigm(con_sg=0, gen_sg=REGenSG.C14, abs_pl=0, con_pl=1, gen_pl=1),
    "b_macave": Paradigm(con_sg=0, gen_sg=REGenSG.C15, abs_pl=0, con_pl=1, gen_pl=1),
    "b_gveret": Paradigm(
        con_sg=0, gen_sg=REGenSG.C16, abs_pl=REAbsPL.C53, con_pl=REConPL.C66, gen_pl=2
    ),
    "b_maskoret": Paradigm(
        con_sg=0, gen_sg=REGenSG.C16, abs_pl=REAbsPL.C43, con_pl=1, gen_pl=1
    ),
    "b_se": Paradigm(
        con_sg=0, gen_sg=REGenSG.C17, abs_pl=0, con_pl=REConPL.C63, gen_pl=1
    ),
    "b_memad": Paradigm(con_sg=0, gen_sg=REGenSG.C18, abs_pl=0, con_pl=1, gen_pl=1),
    "b_par": Paradigm(con_sg=0, gen_sg=REGenSG.C2, abs_pl=0, con_pl=1, gen_pl=1),
    "b_emtsa": Paradigm(
        con_sg=0, gen_sg=REGenSG.C2, abs_pl=0, con_pl=REConPL.C63, gen_pl=1
    ),
    "b_qarqa": Paradigm(
        con_sg=0, gen_sg=REGenSG.C2, abs_pl=0, con_pl=REConPL.C63, gen_pl=2
    ),
    "b_regel": Paradigm(con_sg=0, gen_sg=REGenSG.C3_A, abs_pl=0, con_pl=1, gen_pl=1),
    "b_yerac": Paradigm(
        con_sg=0, gen_sg=REGenSG.C3_A, abs_pl=REAbsPL.C44, con_pl=2, gen_pl=1
    ),
    "b_erets": Paradigm(
        con_sg=0, gen_sg=REGenSG.C3_A, abs_pl=REAbsPL.C44, con_pl=2, gen_pl=2
    ),
    "b_derex": Paradigm(
        con_sg=0, gen_sg=REGenSG.C3_A, abs_pl=REAbsPL.C44, con_pl=REConPL.C64, gen_pl=1
    ),
    "b_delet": Paradigm(
        con_sg=0, gen_sg=REGenSG.C3_A, abs_pl=REAbsPL.C44, con_pl=REConPL.C64, gen_pl=2
    ),
    "b_nexed": Paradigm(
        con_sg=0, gen_sg=REGenSG.C3_E, abs_pl=REAbsPL.C44, con_pl=1, gen_pl=1
    ),
    "b_celeq": Paradigm(
        con_sg=0, gen_sg=REGenSG.C3_E, abs_pl=REAbsPL.C44, con_pl=2, gen_pl=1
    ),
    "b_berex": Paradigm(con_sg=0, gen_sg=REGenSG.C3_I, abs_pl=0, con_pl=1, gen_pl=1),
    "b_sefer": Paradigm(
        con_sg=0, gen_sg=REGenSG.C3_I, abs_pl=REAbsPL.C44, con_pl=2, gen_pl=1
    ),
    "b_shemesh": Paradigm(
        con_sg=0, gen_sg=REGenSG.C3_I, abs_pl=REAbsPL.C44, con_pl=2, gen_pl=2
    ),
    "b_kotel": Paradigm(
        con_sg=0, gen_sg=REGenSG.C3_O, abs_pl=REAbsPL.C44, con_pl=2, gen_pl=1
    ),
    "b_orac": Paradigm(
        con_sg=0, gen_sg=REGenSG.C3_O, abs_pl=REAbsPL.C44, con_pl=2, gen_pl=2
    ),
    "b_rocav": Paradigm(
        con_sg=0, gen_sg=REGenSG.C3_O, abs_pl=REAbsPL.C44, con_pl=REConPL.C67, gen_pl=1
    ),
    "b_qomets": Paradigm(
        con_sg=0, gen_sg=REGenSG.C3_U, abs_pl=REAbsPL.C44, con_pl=2, gen_pl=1
    ),
    "b_tof": Paradigm(con_sg=0, gen_sg=REGenSG.C4, abs_pl=0, con_pl=1, gen_pl=1),
    "b_?1": Paradigm(
        con_sg=0, gen_sg=REGenSG.C4, abs_pl="mAjámA_D", con_pl=1, gen_pl=1
    ),  # FIXME
    "b_ezor": Paradigm(con_sg=0, gen_sg=REGenSG.C5, abs_pl=0, con_pl=1, gen_pl=1),
    "b_piqacat": Paradigm(
        con_sg=0, gen_sg=REGenSG.C30, abs_pl=REAbsPL.C50, con_pl=1, gen_pl=1
    ),
    "b_koteret": Paradigm(
        con_sg=0, gen_sg=REGenSG.C30, abs_pl=REAbsPL.C53, con_pl=REConPL.C63, gen_pl=2
    ),
    "b_atseret": Paradigm(
        con_sg=0, gen_sg=REGenSG.C30, abs_pl=REAbsPL.C53, con_pl=REConPL.C64, gen_pl=2
    ),
    "b_mishqolet": Paradigm(
        con_sg=0, gen_sg=REGenSG.C30, abs_pl=REAbsPL.C43, con_pl=1, gen_pl=1
    ),
    "b_poelet": Paradigm(
        con_sg=0, gen_sg=REGenSG.C30, abs_pl=REAbsPL.C45, con_pl=1, gen_pl=1
    ),
    "b_mavreg": Paradigm(con_sg=0, gen_sg=0, abs_pl=REAbsPL.C45, con_pl=1, gen_pl=1),
    "b_maskelet": Paradigm(
        con_sg=0, gen_sg=REGenSG.C30, abs_pl=REAbsPL.C49, con_pl=1, gen_pl=1
    ),
    "b_maqel": Paradigm(con_sg=0, gen_sg=REGenSG.C7, abs_pl=0, con_pl=1, gen_pl=1),
    "b_i": Paradigm(con_sg=0, gen_sg=REGenSG.C8, abs_pl=0, con_pl=1, gen_pl=1),
    "b_shomer": Paradigm(con_sg=0, gen_sg=REGenSG.C9, abs_pl=0, con_pl=1, gen_pl=1),
    "b_qodqod": Paradigm(
        con_sg=0, gen_sg="qOdqód", abs_pl=0, con_pl=1, gen_pl=1
    ),  # FIXME
    "b_mawet": Paradigm(con_sg=REConSG.C10, gen_sg=0, abs_pl=0, con_pl=1, gen_pl=1),
    "b_zayit": Paradigm(con_sg=REConSG.C11, gen_sg=0, abs_pl=0, con_pl=1, gen_pl=1),
    "b_tayish": Paradigm(
        con_sg=REConSG.C11, gen_sg=0, abs_pl=REAbsPL.C46, con_pl=2, gen_pl=1
    ),
    "b_ayin": Paradigm(
        con_sg=REConSG.C11, gen_sg=0, abs_pl=REAbsPL.C46, con_pl=2, gen_pl=2
    ),
    "b_qoshi": Paradigm(
        con_sg=REConSG.C12, gen_sg=REGenSG.C33, abs_pl=REAbsPL.C44, con_pl=1, gen_pl=1
    ),
    "b_?2": Paradigm(
        con_sg=REConSG.C12, gen_sg=REGenSG.C35, abs_pl=REAbsPL.C47, con_pl=1, gen_pl=1
    ),  # FIXME
    "b_pe": Paradigm(
        con_sg=REConSG.C13, gen_sg=0, abs_pl=REAbsPL.C51, con_pl=1, gen_pl=1
    ),
    "b_zikaron": Paradigm(con_sg=REConSG.C14, gen_sg=0, abs_pl=0, con_pl=1, gen_pl=1),
    "b_gader": Paradigm(
        con_sg=REConSG.C15, gen_sg=REGenSG.C5, abs_pl=0, con_pl=REConPL.C65, gen_pl=1
    ),
    "b_av": Paradigm(
        con_sg=REConSG.C16,
        gen_sg=REGenSG.C12,
        abs_pl=REAbsPL.C42,
        con_pl=REConPL.C63,
        gen_pl=2,
    ),
    "b_ac": Paradigm(
        con_sg=REConSG.C16,
        gen_sg=REGenSG.C12,
        abs_pl="QAj",
        con_pl=REConPL.C63,
        gen_pl=1,
    ),  # FIXME
    "b_dat": Paradigm(
        con_sg=REConSG.C2, gen_sg=REGenSG.C2, abs_pl=0, con_pl=1, gen_pl=1
    ),
    "b_binyan": Paradigm(
        con_sg=REConSG.C2, gen_sg=REGenSG.C2, abs_pl=0, con_pl=REConPL.C63, gen_pl=1
    ),
    "b_kikar": Paradigm(
        con_sg=REConSG.C2, gen_sg=REGenSG.C2, abs_pl=0, con_pl=REConPL.C63, gen_pl=2
    ),
    "b_maacal": Paradigm(
        con_sg=REConSG.C2, gen_sg=REGenSG.C2, abs_pl=0, con_pl=REConPL.C64, gen_pl=1
    ),
    "b_masa": Paradigm(
        con_sg=REConSG.C2, gen_sg=REGenSG.C2, abs_pl=0, con_pl=REConPL.C68, gen_pl=1
    ),
    "b_?3": Paradigm(
        con_sg=REConSG.C2, gen_sg=REGenSG.C2, abs_pl=0, con_pl="maROmd", gen_pl=1
    ),  # FIXME
    "b_aqrav": Paradigm(
        con_sg=REConSG.C2, gen_sg=REGenSG.C4, abs_pl=0, con_pl=1, gen_pl=1
    ),
    "b_paqid": Paradigm(con_sg=REConSG.C3, gen_sg=0, abs_pl=0, con_pl=1, gen_pl=1),
    "b_avel": Paradigm(con_sg=REConSG.C3, gen_sg=0, abs_pl=0, con_pl=1, gen_pl=1),
    "b_qane": Paradigm(
        con_sg=REConSG.C3, gen_sg=0, abs_pl=0, con_pl=REConPL.C63, gen_pl=1
    ),
    "b_sade": Paradigm(
        con_sg=REConSG.C3, gen_sg=0, abs_pl=0, con_pl=REConPL.C63, gen_pl=2
    ),
    "b_caver": Paradigm(
        con_sg=REConSG.C3, gen_sg=0, abs_pl=0, con_pl=REConPL.C64, gen_pl=1
    ),
    "b_aqev": Paradigm(
        con_sg=REConSG.C3, gen_sg=0, abs_pl=0, con_pl=REConPL.C65, gen_pl=1
    ),
    "b_shana": Paradigm(
        con_sg=REConSG.C3, gen_sg=0, abs_pl=REAbsPL.C42, con_pl=2, gen_pl=2
    ),
    "b_saef": Paradigm(
        con_sg=REConSG.C3, gen_sg=REGenSG.C10, abs_pl=0, con_pl=1, gen_pl=1
    ),
    "b_kanaf": Paradigm(
        con_sg=REConSG.C3, gen_sg=REGenSG.C2, abs_pl=0, con_pl=REConPL.C64, gen_pl=1
    ),
    "b_zanav": Paradigm(
        con_sg=REConSG.C3, gen_sg=REGenSG.C2, abs_pl=0, con_pl=REConPL.C64, gen_pl=2
    ),
    "b_davar": Paradigm(
        con_sg=REConSG.C3, gen_sg=REGenSG.C2, abs_pl=0, con_pl=REConPL.C65, gen_pl=1
    ),
    "b_levav": Paradigm(
        con_sg=REConSG.C3, gen_sg=REGenSG.C2, abs_pl=0, con_pl=REConPL.C65, gen_pl=2
    ),
    "b_adom": Paradigm(
        con_sg=REConSG.C3, gen_sg=REGenSG.C4, abs_pl=0, con_pl=1, gen_pl=1
    ),
    "b_ulam": Paradigm(
        con_sg=0, gen_sg=REGenSG.C4, abs_pl=0, con_pl=1, gen_pl=1,
    ),
    "b_catser": Paradigm(
        con_sg=REConSG.C3_A, gen_sg=REGenSG.C5, abs_pl=0, con_pl=REConPL.C64, gen_pl=2
    ),
    "b_zaqen": Paradigm(
        con_sg=REConSG.C3_A, gen_sg=REGenSG.C6, abs_pl=0, con_pl=REConPL.C65, gen_pl=1
    ),
    "b_shxena": Paradigm(
        con_sg=REConSG.C4, gen_sg=0, abs_pl=REAbsPL.C42, con_pl=1, gen_pl=1
    ),
    "b_milcama": Paradigm(
        con_sg=REConSG.C4,
        gen_sg=REGenSG.C30,
        abs_pl=REAbsPL.C42,
        con_pl=REConPL.C63,
        gen_pl=2,
    ),
    "b_atara": Paradigm(
        con_sg=REConSG.C4,
        gen_sg=REGenSG.C30,
        abs_pl=REAbsPL.C42,
        con_pl=REConPL.C64,
        gen_pl=2,
    ),
    "b_ayala": Paradigm(
        con_sg=REConSG.C4,
        gen_sg=REGenSG.C30,
        abs_pl=REAbsPL.C42,
        con_pl=REConPL.C68,
        gen_pl=2,
    ),
    "b_yoleda": Paradigm(
        con_sg=REConSG.C4, gen_sg=REGenSG.C30, abs_pl=REAbsPL.C45, con_pl=1, gen_pl=1
    ),
    "b_tsava": Paradigm(
        con_sg=REConSG.C5, gen_sg=0, abs_pl=0, con_pl=REConPL.C65, gen_pl=2
    ),
    "b_tsali": Paradigm(
        con_sg=REConSG.C5, gen_sg=REGenSG.C8, abs_pl=0, con_pl=1, gen_pl=1
    ),
    "b_mizbeac": Paradigm(
        con_sg=REConSG.C6, gen_sg=REGenSG.C9, abs_pl=0, con_pl=1, gen_pl=1
    ),
    "b_ayir": Paradigm(
        con_sg=REConSG.C7, gen_sg=0, abs_pl=REAbsPL.C46, con_pl=2, gen_pl=1
    ),
    "b_coq": Paradigm(
        con_sg=REConSG.C8, gen_sg=REGenSG.C4, abs_pl=0, con_pl=1, gen_pl=1
    ),
    "b_adama": Paradigm(
        con_sg=REConSG.C9_A, gen_sg=0, abs_pl=REAbsPL.C42, con_pl=2, gen_pl=2
    ),
    "b_arafel": Paradigm(
        con_sg=REConSG.C9_A, gen_sg=REGenSG.C10, abs_pl=0, con_pl=1, gen_pl=1
    ),
    "b_agala": Paradigm(
        con_sg=REConSG.C9_E, gen_sg=0, abs_pl=REAbsPL.C42, con_pl=2, gen_pl=2
    ),
    "b_nedava": Paradigm(
        con_sg=REConSG.C9_I, gen_sg=0, abs_pl=REAbsPL.C42, con_pl=2, gen_pl=2
    ),
    "b_tslatsal": Paradigm(
        con_sg=REConSG.C9_I, gen_sg=REGenSG.C4, abs_pl=0, con_pl=1, gen_pl=1
    ),
    "b_?4": Paradigm(
        con_sg="SWne!Nt", gen_sg=0, abs_pl="SWn3Q", con_pl=1, gen_pl=1
    ),  # FIXME
    "b_yom": Paradigm(
        con_sg=0, gen_sg=0, abs_pl=REAbsPL.C53, con_pl=REConPL.C69, gen_pl=1
    ),
    "b_ir": Paradigm(con_sg=0, gen_sg=0, abs_pl=REAbsPL.C53, con_pl=1, gen_pl=1),
    "b_ish": Paradigm(con_sg=0, gen_sg=0, abs_pl="Qánac", con_pl=REConPL.C64, gen_pl=1),
    "b_ot_neqeva": Paradigm(con_sg=0, gen_sg=0, abs_pl="QWtI_y", con_pl=1, gen_pl=1),
    "b_bat": Paradigm(
        con_sg=0, gen_sg=REGenSG.C10, abs_pl="ban", con_pl=REConPL.C69, gen_pl=2
    ),
    "b_isha": Paradigm(
        con_sg="Qe!cEt", gen_sg="QIcT", abs_pl="nac", con_pl=REConPL.C69, gen_pl=1
    ),
    "b_acot": Paradigm(
        con_sg=REConSG.C3, gen_sg=0, abs_pl="Qácay", con_pl="QAcy", gen_pl=2
    ),
    "b_bayit": Paradigm(
        con_sg=REConSG.C11, gen_sg=0, abs_pl="ba_T", con_pl=1, gen_pl=1
    ),
    "b_ben": Paradigm(
        con_sg="bE!n", gen_sg=REGenSG.C9, abs_pl=REAbsPL.C55, con_pl=2, gen_pl=1
    ),
    "b_shem": Paradigm(
        con_sg=0, gen_sg=REGenSG.C9, abs_pl=REAbsPL.C42, con_pl=2, gen_pl=2
    ),
    "b_dyo": Paradigm(con_sg=0, gen_sg=REGenSG.C19, abs_pl=0, con_pl=1, gen_pl=1),
    "b_tsel": Paradigm(
        con_sg=0, gen_sg=REGenSG.C10, abs_pl="Z3lal", con_pl=REConPL.C65, gen_pl=1
    ),
    "b_matoq": Paradigm(
        con_sg=REConSG.C5, gen_sg="m3tuq", abs_pl=0, con_pl=1, gen_pl=1
    ),
    "b_tsipor": Paradigm(con_sg=0, gen_sg=0, abs_pl="ZI_pór", con_pl=1, gen_pl=1),
    "b_ama": Paradigm(
        con_sg=REConSG.C3, gen_sg=0, abs_pl="Qámah", con_pl=REConPL.C64, gen_pl=2
    ),
    "b_em": Paradigm(
        con_sg=0, gen_sg=REGenSG.C10, abs_pl="QI_mah", con_pl="QI_m3h", gen_pl=2
    ),
    "b_braxa": Paradigm(
        con_sg="bIrk", gen_sg="bIrx", abs_pl=REAbsPL.C42, con_pl=2, gen_pl=2
    ),
    "b_lavi": Paradigm(
        con_sg=REConSG.C3, gen_sg=0, abs_pl=REAbsPL.C53, con_pl=1, gen_pl=1
    ),
    "b_tale": Paradigm(con_sg=REConSG.C3, gen_sg=0, abs_pl="73laQ", con_pl=1, gen_pl=1),
}

SINGULAR_SUFFIX = ["e!H", "a!H", "E!H", "Et", "At", "i!t", "u!t", "A!Qy"] + ["aH"]


def decline_by_paradigm(
    paradigm_id: str, word: str, has_suf: bool, suf_pl: str, throw=False,
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
            paradigm=paradigm_parameters[paradigm_id],
            throw=throw,
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


if __name__ == "__main__":
    print(decline_by_paradigm("b_braxa", "b3raxa!H", True, "W!t"))
    print(decline_by_paradigm("b_em", "Qe!m", False, "W!t"))
