#!/usr/bin/env python3
"""
Parse and validate Proposal IDs (CON vs InfoEd Inst #).

Handles the two-tiered identifier system based on the April 12, 2025 migration.
"""

import re
from datetime import datetime
from typing import Literal, Optional


# Migration date when Syracuse moved from InfoEd to PeopleSoft for pre-award
MIGRATION_DATE = datetime(2025, 4, 12)


def identify_proposal_type(proposal_id: str) -> Literal['CON', 'InfoEd', 'Unknown']:
    """
    Identify whether a Proposal ID is a CON or InfoEd Inst #.
    
    Args:
        proposal_id: The proposal identifier
        
    Returns:
        'CON' if PeopleSoft contract, 'InfoEd' if legacy Inst #, 'Unknown' if neither
        
    Examples:
        >>> identify_proposal_type('CON06743')
        'CON'
        >>> identify_proposal_type('35210')
        'InfoEd'
        >>> identify_proposal_type('ABC123')
        'Unknown'
    """
    if not proposal_id or not isinstance(proposal_id, str):
        return 'Unknown'
    
    # CON format: starts with 'CON' followed by digits
    if re.match(r'^CON\d+$', proposal_id):
        return 'CON'
    
    # InfoEd Inst # format: 5 digits starting with 3
    if re.match(r'^3\d{4}$', proposal_id):
        return 'InfoEd'
    
    return 'Unknown'


def validate_proposal_id(proposal_id: str) -> tuple[bool, Optional[str]]:
    """
    Validate a Proposal ID format.
    
    Args:
        proposal_id: The proposal identifier to validate
        
    Returns:
        Tuple of (is_valid, error_message)
        error_message is None if valid
    """
    if not proposal_id or not isinstance(proposal_id, str):
        return False, "Proposal ID is missing or not a string"
    
    prop_type = identify_proposal_type(proposal_id)
    
    if prop_type == 'Unknown':
        return False, f"Invalid format: '{proposal_id}' (expected CON##### or 3####)"
    
    return True, None


def parse_con_number(proposal_id: str) -> Optional[int]:
    """
    Extract the numeric portion of a CON identifier.
    
    Args:
        proposal_id: CON identifier (e.g., 'CON06743')
        
    Returns:
        Integer CON number, or None if not a valid CON
        
    Example:
        >>> parse_con_number('CON06743')
        6743
    """
    if identify_proposal_type(proposal_id) != 'CON':
        return None
    
    match = re.match(r'^CON(\d+)$', proposal_id)
    if match:
        return int(match.group(1))
    
    return None


def get_submission_era(proposal_id: str, proposal_status: str) -> str:
    """
    Determine when a proposal was likely submitted based on its identifier type.
    
    Args:
        proposal_id: The proposal identifier
        proposal_status: Status (Funded, Not Funded, Pending)
        
    Returns:
        Description of submission era
        
    Notes:
        - CONs can be pre or post migration (all awarded get CONs)
        - InfoEd Inst # means pre-migration and not awarded
    """
    prop_type = identify_proposal_type(proposal_id)
    
    if prop_type == 'InfoEd':
        # InfoEd Inst # only exists for pre-migration unfunded proposals
        return "Pre-April 12, 2025 (InfoEd era, not awarded)"
    
    elif prop_type == 'CON':
        # CONs exist for both eras
        if proposal_status == 'Funded':
            return "Any era (awarded proposals always get CONs)"
        elif proposal_status == 'Pending':
            # Could be either era, but likely post-migration
            return "Likely post-April 12, 2025 (PeopleSoft era)"
        else:  # Not Funded
            # Not funded CONs are post-migration
            return "Post-April 12, 2025 (PeopleSoft era, not awarded)"
    
    return "Unknown era"


def format_proposal_id(proposal_id: str) -> str:
    """
    Format a Proposal ID for display with type indicator.
    
    Args:
        proposal_id: The proposal identifier
        
    Returns:
        Formatted string with type indicator
        
    Example:
        >>> format_proposal_id('CON06743')
        'CON06743 (PeopleSoft Contract)'
        >>> format_proposal_id('35210')
        '35210 (InfoEd Inst #)'
    """
    prop_type = identify_proposal_type(proposal_id)
    
    if prop_type == 'CON':
        return f"{proposal_id} (PeopleSoft Contract)"
    elif prop_type == 'InfoEd':
        return f"{proposal_id} (InfoEd Inst #)"
    else:
        return f"{proposal_id} (Unknown Type)"


if __name__ == '__main__':
    # Test cases
    test_ids = [
        'CON06743',
        'CON04855',
        '35210',
        '35199',
        'ABC123',
        '',
        None
    ]
    
    print("PROPOSAL ID PARSER TESTS")
    print("=" * 80)
    
    for pid in test_ids:
        print(f"\nProposal ID: {repr(pid)}")
        
        # Identify type
        prop_type = identify_proposal_type(str(pid) if pid else '')
        print(f"  Type: {prop_type}")
        
        # Validate
        is_valid, error = validate_proposal_id(str(pid) if pid else '')
        if is_valid:
            print(f"  Valid: [OK]")
            print(f"  Formatted: {format_proposal_id(str(pid))}")
            
            # For CONs, extract number
            if prop_type == 'CON':
                con_num = parse_con_number(str(pid))
                print(f"  CON Number: {con_num}")
            
            # Show submission era examples
            for status in ['Funded', 'Pending', 'Not Funded']:
                era = get_submission_era(str(pid), status)
                print(f"  Era (if {status}): {era}")
        else:
            print(f"  Valid: [NO] - {error}")
