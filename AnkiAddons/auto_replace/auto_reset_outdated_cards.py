from aqt import mw
from aqt.utils import showInfo, showWarning


def reset_cards():
    """Reset cards according to the current Anki profile."""

    YEAR_IN_DAYS = 365
    HALF_YEAR_IN_DAYS = int(YEAR_IN_DAYS / 2) # 182 days
    TWO_YEARS_IN_DAYS = 2 * YEAR_IN_DAYS # 730 days
    FOUR_YEARS_IN_DAYS = 4 * YEAR_IN_DAYS # 1460 days

    queries = {
        # Temporarily excluded some decks from the general search; over time, these decks should be included
        # "!Foreign Languages": f'prop:ivl>={TWO_YEARS_IN_DAYS} -deck:English -deck:"Languages. Greek !Words" -deck:"Languages. Latin"',
        "!Foreign Languages": (
            # более общее правило: не допускает карточки старше 4-х лет в любом из деков
            f'(prop:ivl>={FOUR_YEARS_IN_DAYS}) OR '
            
            # более специфичное правило: не допускает карточки старше 2-х лет во всех деках, кроме указанных
            f'(prop:ivl>={TWO_YEARS_IN_DAYS} -deck:English -deck:"Languages. Greek !Words" -deck:"Languages. Latin")'
        ),

        # Two search conditions are used here:
        # 1) a more general/gentle one for all cards and
        # 2) a more specific/strict one for 'Java' deck.
        "Deutsch": f'(prop:ivl>={TWO_YEARS_IN_DAYS}) OR (deck:"Java" prop:ivl>={HALF_YEAR_IN_DAYS})',

        "IT": f"prop:ivl>={TWO_YEARS_IN_DAYS}",
        "Orthodoxy": f"prop:ivl>={TWO_YEARS_IN_DAYS}",
    }

    profile = mw.pm.name

    if profile not in queries:
        showWarning(
            f"No reset rule is configured for the profile “{profile}”."
        )
        return

    query = queries[profile]
    card_ids = mw.col.find_cards(query)

    if not card_ids:
        showInfo(
            f"Profile: {profile}\n"
            f"Query: {query}\n\n"
            "No cards to reset."
        )
        return

    # showInfo(f'Number of cards to reset: {len(card_ids)}')

    mw.col.sched.reset_cards(card_ids)
    mw.reset()

    showInfo(
        f"Profile: {profile}\n"
        f"Query: {query}\n\n"
        f"Cards reset: {len(card_ids)}"
    )