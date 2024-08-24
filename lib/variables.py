from typing import List


class Element:
    H, He, Li, Be, B, C, N, O, F, Ne, Na, Mg, Al, Si, P = list(range(1, 16))
    S, Cl, Ar, K, Ca, Sc, Ti, V, Cr, Mn, Fe, Co, Ni, Cu, Zn = list(range(16, 31))
    Ga, Ge, As, Se, Br, Kr, Rb, Sr, Y, Zr, Nb, Mo, Tc, Ru = list(range(31, 45))
    Rh, Pd, Ag, Cd, In, Sn, Sb, Te, I, Xe, Cs, Ba, La, Ce = list(range(45, 59))
    Pr, Nd, Pm, Sm, Eu, Gd, Tb, Dy, Ho, Er, Tm, Yb, Lu, Hf = list(range(59, 73))
    Ta, W, Re, Os, Ir, Pt, Au, Hg, Tl, Pb, Bi, Po, At, Rn = list(range(73, 87))
    Fr, Ra, Ac, Th, Pa, U, Np, Pu, Am, Cm, Bk, Cf, Es, Fm = list(range(87, 101))
    Md, No, Lr, Rf, Db, Sg, Bh, Hs, Mt, Ds, Rg, Cn, Uut = list(range(101, 114))
    Fl, Uup, Lv, Uus, Uuo = list(range(114, 119))

    @staticmethod
    def map_atom_radii_dict(atom_radiis_dict: List[dict]):
        mapped_atom_radii = {}
        for atom_dict in atom_radiis_dict:
            mapped_atom_radii[getattr(Element, list(atom_dict.keys())[0])] = list(atom_dict.values())[0]
        return mapped_atom_radii
