"""
This example shows how to get match substitutions.

The output will be something like:

Vinícius Jr. is substituted by Endrick at 115'
R. Mandava is substituted by C. Azpilicueta at 98'
C. Lenglet is substituted by R. Le Normand at 91'
R. de Paul is substituted by N. Molina at 90'
A. Griezmann is substituted by A. Sørloth at 89'
G. Simeone is substituted by Á. Correa at 89'
C. Gallagher is substituted by S. Lino at 85'
F. Mendy is substituted by F. Garcia at 83'
Rodrygo is substituted by B. Díaz at 79'
L. Modrić is substituted by L. Vázquez at 65'
A. Tchouaméni is substituted by E. Camavinga at 65'

"""

from esd.sofascore import SofascoreClient, IncidentType

client = SofascoreClient()

# A. Madrid vs. Real Madrid
incidents = client.get_match_incidents(13511924)

for incident in incidents:

    if incident.type != IncidentType.SUBSTITUTION:
        continue

    print(
        f"{incident.player_out.short_name} is substituted by {incident.player_in.short_name} at {incident.time}'"
    )
