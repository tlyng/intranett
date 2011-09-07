# -*- coding: utf-8 -*-

from Products.ATContentTypes.lib import constraintypes
from Products.CMFCore.utils import getToolByName
from zope.publisher.browser import BrowserView


class DefaultContent(BrowserView):

    def __call__(self):
        wf = getToolByName(self.context, 'portal_workflow')
        portal_url = getToolByName(self.context, 'portal_url')
        site = portal_url.getPortalObject()

        # Aktuelt og nytt folder
        site.invokeFactory('Folder',
            id='aktuelt',
            title='Aktuelt og nytt',
            description='Nyheter og oppdateringer på intranettet.')
        aktuelt = site['aktuelt']
        aktuelt.processForm()
        wf.doActionFor(aktuelt, 'publish')
        aktuelt.reindexObject()

        # Initial news item
        aktuelt.invokeFactory('News Item',
            id='nytt-intranett',
            title='Nytt intranett',
            description='Det nye intranettet er klart til bruk.',
            text=NYTT_INTRANETT,
            text_format='html')
        nytt_intranett = aktuelt['nytt-intranett']
        nytt_intranett.processForm()
        wf.doActionFor(nytt_intranett, 'publish')
        nytt_intranett.reindexObject()

        # prosjekter
        site.invokeFactory('Folder',
            id='prosjekter',
            title='Prosjekter',
            description='Mappe for prosjekter')
        prosjekter = site['dokumenter']
        prosjekter.setConstrainTypesMode(constraintypes.ENABLED)
        prosjekter.setLocallyAllowedTypes(['TeamWorkspace'])
        prosjekter.setImmediatelyAddableTypes(['TeamWorkspace'])
        prosjekter.processForm()
        wf.doActionFor(prosjekter, 'publish')
        prosjekter.reindexObject()

        # dokumenter folder
        site.invokeFactory('Folder',
            id='dokumenter',
            title='Dokumenter',
            description='Mappe for dokumenter')
        dokumenter = site['dokumenter']
        dokumenter.processForm()
        wf.doActionFor(dokumenter, 'publish')
        dokumenter.reindexObject()

        # Grunnleggende bruk page
        dokumenter.invokeFactory('Document',
            id='grunnleggende-bruk',
            title='Grunnleggende bruk',
            description='Kom i gang med bruk av intranettet. '
            '(Dette innholdet er hentet fra hjelp.intranett.no og kan slettes når det ikke er behov for lengre)',
            text=GRUNNLEGGENDE_BRUK,
            text_format='html')
        grunnleggende_bruk = dokumenter['grunnleggende-bruk']
        grunnleggende_bruk.processForm()
        wf.doActionFor(grunnleggende_bruk, 'publish')
        grunnleggende_bruk.reindexObject()

        # Go to frontpage
        self.request.response.redirect(site.absolute_url())
        return 'done'


NYTT_INTRANETT="""\
<p>Intranettet lar oss dele dokumenter, tekst, bilder, nyheter og
interninformasjon på en lettvint måte.</p>
<p>Du kan nå intranettet overalt hvor du har internett-tilgang.</p>
"""

GRUNNLEGGENDE_BRUK = """\
<p>Intranettet har "innhold" av forskjellige typer, for eksempel
nyhetsartikler, bilder, filer og sider. Det er personen som legger til
innholdet som bestemmer hva slags type det er.</p>
<p>Når noen har lagt til innhold, og publisert det, vil det være synlig for de
andre brukerne av intranettet. Det vil dukke opp i menyene og i relevante
søkeresultater.</p>
<p>Innholdet er ordnet i mapper, akkurat som man gjør på sin egen datamaskin.
Det er mappene som bestemmer hva menystrukturen blir.</p>
<h3>Brukerkonto</h3>
<p>For å kunne se intranettet må du ha en brukerkonto. Brukerkontoen er
personlig og har et eget brukernavn og et passord bare for deg.</p>
<p>Du må bruke brukernavnet og passordet sammen for å kunne logge inn på
intranettet. Det er viktig at du ikke deler brukerkontoen din og passordet ditt
med andre.</p>
<p>Personer uten brukerkonto har ikke tilgang til intranettet.</p>
<h3>Tilgangskontroll</h3>
<p>Forskjellige brukerkontoer kan ha forskjellige tilgangsrettigheter i
forskjellige mapper. Om du ikke har tilgang til å se en mappe, vil den ikke
være synlig for deg.</p>
<p>Noen brukere har lov å legge til eller redigere innhold.
Administratorbrukere kan legge til eller endre innhold overalt i intranettet,
mens andre brukere gjerne får tildelt muligheten til å legge til innhold i en
egen mappe eller en mappe for sin avdeling.</p>
<h3>Organisering av intranettet</h3>
<p>Utgangspunktet for organiseringen av innhold på intranett.no er en vanlig
mappestruktur.</p>
<p>Mapper på toppnivå eller rot vil automatisk danne toppmenyen på ditt
intranett. Vanlige eller mye brukte toppmenypunkter er:</p>
<p>Nyheter - Aktuelt - Siste nytt - Ansatte</p>
<p>Hendelser - Hva skjer? - Ansatte</p>
<p>Prosjekter - Dokumenter - Kunder - Leverandører - Ansatte</p>
<p>HR - Rutiner - Skjemaer - Ansatte</p>
<p>Det finnes ikke noe rett eller galt når det gjelder organsieringen av
intranettet, kun hva som passer hver og en organisasjon. Intranettet er heller
ikke statisk, men utvikles og tilpasses over tid.</p>
"""
