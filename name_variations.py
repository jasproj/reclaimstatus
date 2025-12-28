"""
Treasury Package - Complete Name Variations Generator

Based on analysis of all 24 documents, these are ALL name formats used.
The system must generate every variation to establish legal superiority.
"""

def generate_all_name_variations(first: str, middle: str, last: str, suffix: str = "") -> dict:
    """
    Generate ALL name variations from a single name entry.
    
    Documents analyzed:
    - Hold Harmless & Indemnity Agreement
    - Security Agreement  
    - Copyright Affidavit
    - Common Law Copyright Notice
    - Act of Expatriation
    - Power of Attorney
    - International Registered Private Tracking
    - Appointment of Fiduciary
    
    Args:
        first: First name (e.g., "Thomas")
        middle: Middle name (e.g., "Kallen") - can be empty
        last: Last name (e.g., "Claycomb")
        suffix: Optional suffix (e.g., "Jr", "Sr", "III")
    
    Returns:
        Dictionary with all name variations categorized by type
    """
    
    # Clean inputs
    first = first.strip()
    middle = middle.strip() if middle else ""
    last = last.strip()
    suffix = suffix.strip() if suffix else ""
    
    # Get initials
    f_init = first[0].upper() if first else ""
    m_init = middle[0].upper() if middle else ""
    l_init = last[0].upper() if last else ""
    
    # Suffix handling
    suffix_upper = suffix.upper()
    suffix_part = f" {suffix}" if suffix else ""
    suffix_part_upper = f" {suffix_upper}" if suffix else ""
    
    variations = {
        # ============================================================
        # DEBTOR / ALL CAPS VARIATIONS (Legal Fiction / Strawman)
        # Used in: Security Agreement, Hold Harmless, Copyright docs
        # ============================================================
        "debtor_variations": {
            # Full name - all caps
            "FULL_CAPS": f"{first.upper()} {middle.upper()} {last.upper()}{suffix_part_upper}".strip(),
            
            # Without middle name
            "CAPS_NO_MIDDLE": f"{first.upper()} {last.upper()}{suffix_part_upper}",
            
            # Middle initial only
            "CAPS_MIDDLE_INIT": f"{first.upper()} {m_init} {last.upper()}{suffix_part_upper}".replace("  ", " "),
            
            # First initial + middle + last
            "CAPS_FIRST_INIT": f"{f_init} {middle.upper()} {last.upper()}{suffix_part_upper}".strip() if middle else None,
            
            # First initial only
            "CAPS_INIT_LAST": f"{f_init} {last.upper()}{suffix_part_upper}",
            
            # Middle first (reversed) - found in Act of Expatriation
            "CAPS_REVERSED": f"{middle.upper()} {first.upper()} {last.upper()}{suffix_part_upper}".strip() if middle else None,
            
            # Initials only (2 letter)
            "INITIALS_TWO": f"{f_init}{l_init}",
            
            # Initials only (3 letter) 
            "INITIALS_THREE": f"{f_init}{m_init}{l_init}" if middle else f"{f_init}{l_init}",
            
            # Two initials + last name
            "CAPS_TWO_INIT_LAST": f"{f_init}{m_init} {last.upper()}{suffix_part_upper}" if middle else f"{f_init} {last.upper()}{suffix_part_upper}",
            
            # Last name only
            "CAPS_LAST_ONLY": f"{last.upper()}",
            
            # First + last initial
            "CAPS_FIRST_LAST_INIT": f"{first.upper()} {l_init}",
            
            # Comma format (Last, First Middle)
            "CAPS_COMMA": f"{last.upper()}, {first.upper()} {middle.upper()}".strip().rstrip(","),
            
            # Comma format (Last, First M)
            "CAPS_COMMA_INIT": f"{last.upper()}, {first.upper()} {m_init}".strip().rstrip(",") if middle else f"{last.upper()}, {first.upper()}",
        },
        
        # ============================================================
        # CREDITOR / STYLED VARIATIONS (Living Man / Secured Party)
        # Uses special punctuation: hyphen between first-middle, colon before last
        # ============================================================
        "creditor_variations": {
            # Primary styled format (First-Middle: Last)
            "STYLED_FULL": f"{first}-{middle}: {last}{suffix_part}" if middle else f"{first}: {last}{suffix_part}",
            
            # Mixed case full name
            "MIXED_FULL": f"{first} {middle} {last}{suffix_part}".strip(),
            
            # Mixed case no middle
            "MIXED_NO_MIDDLE": f"{first} {last}{suffix_part}",
            
            # Mixed with middle initial + period
            "MIXED_MIDDLE_INIT": f"{first} {m_init}. {last}{suffix_part}".replace(" . ", " ") if middle else f"{first} {last}{suffix_part}",
            
            # First initial + middle + last (mixed)
            "MIXED_FIRST_INIT": f"{f_init} {middle} {last}{suffix_part}" if middle else None,
            
            # Dotted initials
            "MIXED_DOTTED_INIT": f"{f_init}.{m_init}. {last}{suffix_part}" if middle else f"{f_init}. {last}{suffix_part}",
            
            # First + Last only (title case)
            "MIXED_SIMPLE": f"{first} {last}",
            
            # Initial period format
            "MIXED_INIT_PERIOD": f"{f_init}. {middle} {last}{suffix_part}" if middle else f"{f_init}. {last}{suffix_part}",
        },
        
        # ============================================================
        # TRUST VARIATIONS
        # Used in Copyright Notice, Security Agreement
        # ============================================================
        "trust_variations": {
            # Trust full name
            "TRUST_FULL": f"{first.upper()} {middle.upper()} {last.upper()} TRUST".strip(),
            
            # Trust with copyright symbol
            "TRUST_COPYRIGHT": f"{first.upper()} {middle.upper()} {last.upper()} TRUST©".strip(),
            
            # Trust initials
            "TRUST_INITIALS": f"{f_init}{m_init}{l_init} TRUST" if middle else f"{f_init}{l_init} TRUST",
        },
        
        # ============================================================
        # COPYRIGHT/TRADEMARK VARIATIONS  
        # Used in Copyright Affidavit
        # ============================================================
        "copyright_variations": {
            # Name with copyright symbol
            "COPYRIGHT_FULL": f"{first.upper()} {middle.upper()} {last.upper()}©".strip(),
            
            # Quoted format
            "QUOTED_CAPS": f'"{first.upper()} {middle.upper()} {last.upper()}"'.strip(),
            
            # Single quoted styled
            "QUOTED_STYLED": f"'{first}-{middle}: {last}'" if middle else f"'{first}: {last}'",
        },
        
        # ============================================================
        # SPECIAL DOCUMENT FORMATS
        # ============================================================
        "special_formats": {
            # "one [Name], Free man" format (International Tracking)
            "FREE_MAN": f"one {first}-{middle}: {last}, Free man" if middle else f"one {first}: {last}, Free man",
            
            # Attorney in Fact format
            "ATTORNEY_IN_FACT": f"{first}-{middle}: {last}, Attorney in Fact" if middle else f"{first}: {last}, Attorney in Fact",
            
            # Secured Party Creditor format
            "SECURED_PARTY": f"{first}-{middle}: {last}, Secured Party Creditor" if middle else f"{first}: {last}, Secured Party Creditor",
            
            # Third Party Intervener format (Appointment of Fiduciary)
            "THIRD_PARTY": f"{first}-{middle}: {last}, Third Party Interest Intervener" if middle else f"{first}: {last}, Third Party Interest Intervener",
            
            # Bailor format (Hold Harmless)
            "BAILOR": f"{first}-{middle}: {last}, Bailor" if middle else f"{first}: {last}, Bailor",
            
            # Bailee format (all caps)
            "BAILEE": f"{first.upper()} {middle.upper()} {last.upper()}, BAILEE".strip(),
            
            # Agent format
            "AGENT": f"{first}-{middle}: {last}, Agent" if middle else f"{first}: {last}, Agent",
            
            # Beneficiary format  
            "BENEFICIARY": f"{first}-{middle}: {last}, Beneficiary" if middle else f"{first}: {last}, Beneficiary",
            
            # Principal format
            "PRINCIPAL": f"{first}-{middle}: {last}, Principal" if middle else f"{first}: {last}, Principal",
            
            # Grantor format
            "GRANTOR": f"{first.upper()} {middle.upper()} {last.upper()}, GRANTOR".strip(),
            
            # Indemnitee format
            "INDEMNITEE": f"{first}-{middle}: {last}, Indemnitee" if middle else f"{first}: {last}, Indemnitee",
            
            # Indemnitor format (all caps)
            "INDEMNITOR": f"{first.upper()} {middle.upper()} {last.upper()}, INDEMNITOR".strip(),
        },
        
        # ============================================================
        # ADDRESS LINE FORMATS
        # ============================================================
        "address_formats": {
            # c/o format
            "C_O_STYLED": f"c/o {first}-{middle}: {last}" if middle else f"c/o {first}: {last}",
            
            # Attention format
            "ATTN_CAPS": f"ATTN: {first.upper()} {middle.upper()} {last.upper()}".strip(),
        },
        
        # ============================================================
        # DOCUMENT REFERENCE CODES
        # Based on initials - used for file numbers
        # ============================================================
        "reference_codes": {
            # 3-letter code
            "CODE_THREE": f"{f_init}{m_init}{l_init}" if middle else f"{f_init}{l_init}",
            
            # 2-letter code  
            "CODE_TWO": f"{f_init}{l_init}",
            
            # File prefix (for document numbering)
            "FILE_PREFIX": f"{f_init}{m_init}{l_init}" if middle else f"{f_init}{l_init}",
        },
        
        # ============================================================
        # ADDITIONAL VARIATIONS FOUND IN DOCUMENTS
        # ============================================================
        "additional_variations": {
            # D.B.A format (doing business as)
            "DBA_CAPS": f"{first.upper()} {middle.upper()} {last.upper()}".strip(),
            
            # A.K.A format (also known as)  
            "AKA_CAPS": f"{first.upper()} {middle.upper()} {last.upper()}".strip(),
            
            # Ens Legis format (legal entity)
            "ENS_LEGIS": f"{first.upper()} {middle.upper()} {last.upper()}, Ens legis".strip(),
            
            # Living Soul format
            "LIVING_SOUL": f"{first}-{middle}: {last}, a Living Soul" if middle else f"{first}: {last}, a Living Soul",
            
            # Natural Man format
            "NATURAL_MAN": f"{first}-{middle}: {last}, a Natural Man" if middle else f"{first}: {last}, a Natural Man",
            
            # Flesh and Blood format (from documents)
            "FLESH_BLOOD": f"{first}-{middle}: {last}, a living, flesh-and-blood man" if middle else f"{first}: {last}, a living, flesh-and-blood man",
            
            # Authorized Representative format
            "AUTH_REP": f"{first}-{middle}: {last}, Authorized Representative" if middle else f"{first}: {last}, Authorized Representative",
            
            # Holder in Due Course
            "HOLDER_DUE_COURSE": f"{first}-{middle}: {last}, Holder in Due Course" if middle else f"{first}: {last}, Holder in Due Course",
            
            # Executor format
            "EXECUTOR": f"{first}-{middle}: {last}, Executor" if middle else f"{first}: {last}, Executor",
            
            # Settlor format  
            "SETTLOR": f"{first}-{middle}: {last}, Settlor" if middle else f"{first}: {last}, Settlor",
            
            # Trustee format
            "TRUSTEE": f"{first}-{middle}: {last}, Trustee" if middle else f"{first}: {last}, Trustee",
            
            # Private Contract Trust format
            "PRIVATE_TRUST": f"{first}-{middle}: {last} Secured Party Private Contract Trust" if middle else f"{first}: {last} Secured Party Private Contract Trust",
            
            # Real Party in Interest
            "REAL_PARTY": f"{first}-{middle}: {last}, a Real Party in Interest" if middle else f"{first}: {last}, a Real Party in Interest",
            
            # Transmitting Utility (DEBTOR function)
            "TRANSMITTING_UTILITY": f"{first.upper()} {middle.upper()} {last.upper()}".strip(),
            
            # Personam Sojourn format
            "PERSONAM_SOJOURN": f"{first}-{middle}: {last}, Personam Sojourn" if middle else f"{first}: {last}, Personam Sojourn",
            
            # American State National
            "STATE_NATIONAL": f"{first}-{middle}: {last}, American State National" if middle else f"{first}: {last}, American State National",
            
            # Non-Domestic format
            "NON_DOMESTIC": f"{first}-{middle}: {last}, Non-Domestic" if middle else f"{first}: {last}, Non-Domestic",
            
            # Creditor Bailor combined
            "CREDITOR_BAILOR": f"{first}-{middle}: {last}, Creditor/Bailor" if middle else f"{first}: {last}, Creditor/Bailor",
            
            # Debtor Bailee combined (caps)
            "DEBTOR_BAILEE": f"{first.upper()} {middle.upper()} {last.upper()}, DEBTOR/BAILEE".strip(),
            
            # For: format (used in signatures)
            "FOR_DEBTOR": f"For: {first.upper()} {middle.upper()} {last.upper()}, DEBTOR".strip(),
            
            # By: format with styled name
            "BY_STYLED": f"By: {first}-{middle}: {last}" if middle else f"By: {first}: {last}",
            
            # Estate format
            "ESTATE": f"[{first.upper()} {middle.upper()} {last.upper()}] ESTATE".strip(),
        }
    }
    
    # Remove None values
    for category in variations:
        variations[category] = {k: v for k, v in variations[category].items() if v is not None}
    
    return variations


def get_flat_variations(first: str, middle: str, last: str, suffix: str = "") -> dict:
    """
    Get all variations as a flat dictionary for easy replacement.
    """
    all_vars = generate_all_name_variations(first, middle, last, suffix)
    
    flat = {}
    for category, vars_dict in all_vars.items():
        flat.update(vars_dict)
    
    return flat


def print_variations_report(first: str, middle: str, last: str, suffix: str = ""):
    """Print a formatted report of all name variations."""
    
    variations = generate_all_name_variations(first, middle, last, suffix)
    
    print("=" * 70)
    print(f"NAME VARIATIONS REPORT")
    print(f"Input: {first} {middle} {last} {suffix}".strip())
    print("=" * 70)
    
    for category, vars_dict in variations.items():
        print(f"\n### {category.upper().replace('_', ' ')} ###")
        for key, value in vars_dict.items():
            print(f"  {key:25} : {value}")
    
    # Count total
    total = sum(len(v) for v in variations.values())
    print(f"\n{'=' * 70}")
    print(f"TOTAL VARIATIONS: {total}")
    print("=" * 70)


# ============================================================
# TEST
# ============================================================
if __name__ == "__main__":
    # Test with Thomas Kallen Claycomb
    print_variations_report("Thomas", "Kallen", "Claycomb")
    
    print("\n\n")
    
    # Test without middle name
    print_variations_report("John", "", "Smith")
    
    print("\n\n")
    
    # Test with suffix
    print_variations_report("Robert", "James", "Williams", "Jr")
