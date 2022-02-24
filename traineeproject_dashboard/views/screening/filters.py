from edc_dashboard.listboard_filter import ListboardFilter, ListboardViewFilters


class CustomListboardViewFilters(ListboardViewFilters):
    all = ListboardFilter(
        name='all',
        label='All',
        lookup={})

    eligible = ListboardFilter(
        name='eligible',
        label='Eligible',
        lookup={'is_eligible': True}
    )

    not_eligible = ListboardFilter(
        name='not_eligible',
        label='Not Eligible',
        lookup={'is_eligible': False}
    )

    consented = ListboardFilter(
        label='Consented',
        position=20,
        lookup={'is_eligible': True,
                'consented': True})

    not_consented = ListboardFilter(
        label='Not consented',
        position=21,
        lookup={'is_eligible': True,
                'consented': False})