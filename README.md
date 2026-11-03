# Microsoft Teams Presence — Home Assistant

Niestandardowa integracja Home Assistant, która pobiera status zalogowanego użytkownika Microsoft 365 z Microsoft Graph. Tworzy jeden sensor ze stanem `online`, `away`, `busy`, `on_meeting` albo `offline`. Odświeża dane co 60 sekund.

Mapowanie: `Available` → `online`; `Away`/`BeRightBack` → `away`; `Busy`/`DoNotDisturb` → `busy`; `Busy` + aktywność `InAMeeting` → `on_meeting`; `Offline` → `offline`.

## Ograniczenia

- Integracja odczytuje wyłącznie status konta, które łączy się z Microsoftem.
- Wymagane jest konto służbowe/szkolne Microsoft 365. Osobiste konta Microsoft nie obsługują tego endpointu Graph.
- Administrator Microsoft Entra może ograniczyć zgodę użytkownika na uprawnienia aplikacji.

## Instalacja

Skopiuj folder `custom_components/teams_presence` do katalogu `config/custom_components/` Home Assistanta i uruchom ponownie Home Assistant.

### Przez HACS

Dodaj `https://github.com/pawelczykkacper/teams` jako repozytorium niestandardowe typu **Integration**, wybierz najnowszą wersję z domyślnej gałęzi i zainstaluj. Następnie uruchom ponownie Home Assistant. Wersja `1726a9d` nie zawierała wymaganego pliku `hacs.json`; po dodaniu repozytorium ponownie pobierz najnowszą wersję.

## Rejestracja aplikacji Microsoft

1. W Microsoft Entra ID utwórz rejestrację aplikacji typu **Accounts in any organizational directory**.
2. Dodaj platformę **Web** i URI przekierowania Home Assistanta:
   `https://my.home-assistant.io/redirect/oauth`
3. Utwórz sekret klienta w **Certificates & secrets**.
4. W **API permissions** dodaj Microsoft Graph → **Delegated permissions** → `Presence.Read`.
5. Nie dodawaj uprawnień zapisu ani `Presence.Read.All`.
6. Skopiuj **Application (client) ID** i wartość sekretu klienta.

## Konfiguracja Home Assistant

1. W **Ustawienia → Urządzenia i usługi → Poświadczenia aplikacji** dodaj poświadczenie Microsoft Teams Presence, wklejając Client ID i sekret klienta.
2. Otwórz **Ustawienia → Urządzenia i usługi → Dodaj integrację → Microsoft Teams Presence**.
3. Zaloguj się kontem organizacyjnym Microsoft 365 i zaakceptuj `Presence.Read`.

Integracja tworzy sensor statusu. „Na spotkaniu” jest rozpoznawane po kombinacji Graph `Busy / InAMeeting`; Teams może potrzebować kilku minut, by zaktualizować obecność w Graph. OAuth odświeża token automatycznie.

## Dane z Microsoft Graph

Integracja używa `GET https://graph.microsoft.com/v1.0/me/presence` i normalizuje pola `availability` oraz `activity` do jednego stanu.
