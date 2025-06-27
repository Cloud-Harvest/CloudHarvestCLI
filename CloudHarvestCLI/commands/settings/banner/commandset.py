from rich.text import Text

def do_banner(args):
    from CloudHarvestCLI.configuration import HarvestConfiguration
    _banners = HarvestConfiguration.banners

    from CloudHarvestCLI.banner import get_banner

    if args.names:
        names = args.names

    else:
        names = {name: config for name, config in _banners.items() if not str(name).startswith('.')}

    results = {
        name: get_banner(banner_configuration=_banners,
                         name=name,
                         text=args.text)
        for name in names
    }

    for name, banner in results.items():
        from CloudHarvestCLI.text import console
        console.print(f'\n {name}----------')
        console.print(banner[0])
        if banner[2]:
            console.print(_rules_to_text(banner[2]))

def _rules_to_text(rules: list) -> (Text, str):
    footer = []

    def day_part_as_int(day_part: int) -> str:
        if isinstance(day_part, str):
            return day_part
        else:
            return str(day_part).zfill(2)

    # formatting for rule outputs
    for rule in (rules or []):
        if rule.get('date', {}).get('between'):
            r = 'date between: "YYYY-%s-%s" and "YYYY-%s-%s":' % (
                day_part_as_int(rule['date']['between']['start']['month']),
                day_part_as_int(rule['date']['between']['start'].get('day', '*')),
                day_part_as_int(rule['date']['between']['end']['month']),
                day_part_as_int(rule['date']['between']['end'].get('day', '*')),
            )

        else:
            r = 'date: "YYYY-%s-%s":' % (
                day_part_as_int(rule.get('date', {}).get('month', '*')),
                day_part_as_int(rule.get('date', {}).get('day', '*')),
            )

        r += '\n' + rule.get('footer', '(no footer)')
        footer.append(r)

    footer = '\n'.join(footer)

    return footer
