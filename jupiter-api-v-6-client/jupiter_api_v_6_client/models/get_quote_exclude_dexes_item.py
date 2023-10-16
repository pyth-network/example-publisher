from enum import Enum


class GetQuoteExcludeDexesItem(str, Enum):
    ALDRIN = "Aldrin"
    ALDRIN_V2 = "Aldrin V2"
    BALANSOL = "Balansol"
    BONKSWAP = "Bonkswap"
    CREMA = "Crema"
    CROPPER = "Cropper"
    FLUXBEAM = "FluxBeam"
    HELIUM_NETWORK = "Helium Network"
    INVARIANT = "Invariant"
    JUPITER_LO = "Jupiter LO"
    LIFINITY_V1 = "Lifinity V1"
    LIFINITY_V2 = "Lifinity V2"
    MARINADE = "Marinade"
    MERCURIAL = "Mercurial"
    METEORA = "Meteora"
    OASIS = "Oasis"
    OPENBOOK = "Openbook"
    ORCA_V1 = "Orca V1"
    ORCA_V2 = "Orca V2"
    PENGUIN = "Penguin"
    PHOENIX = "Phoenix"
    RAYDIUM = "Raydium"
    RAYDIUM_CLMM = "Raydium CLMM"
    SABER = "Saber"
    SABER_DECIMALS = "Saber (Decimals)"
    SANCTUM = "Sanctum"
    SAROS = "Saros"
    STEPN = "StepN"
    SYMMETRY = "Symmetry"
    WHIRLPOOL = "Whirlpool"

    def __str__(self) -> str:
        return str(self.value)
