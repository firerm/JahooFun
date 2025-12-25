# 🤣 Daily Cartoon Card για Home Assistant

Ένα απλό integration/custom sensor για το Home Assistant που φέρνει την γελοιογραφία της ημέρας απευθείας στο Lovelace Dashboard σας, προσθέτοντας μια δόση χιούμορ στην καθημερινή σας ρουτίνα.

## 🚀 Εγκατάσταση

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=firerm&repository=JahooFun&category=intergration)

## 🖼️ Lovelace YAML Configuration

Χρησιμοποιήστε τον ακόλουθο κώδικα YAML σε μία κάρτα **Manual** στο Lovelace Dashboard σας. Η διάταξη χρησιμοποιεί ένα `vertical-stack` για να συνδυάσει την εικόνα και τα συνοδευτικά στοιχεία κειμένου/συνδέσμων.

Aν θέλετε φτιάξτε ένα WebPage και βάλντε αυτή την URL : [
](https://jahoo.gr/jf/?mode=widget) είναι ο πιο απλό τρόπος !
### Κώδικας Κάρτας

```yaml
type: vertical-stack
cards:
  # 1. Image Card (Using Camera Entity)
  - type: picture-entity
    entity: camera.jf_daily_cartoon
    show_name: false
    show_state: false
    # Aspect Ratio removed to allow "contain" behavior (full image visible)
    tap_action:
      action: none

  # 2. Text & Content (Using Sensor Entity)
  - type: markdown
    content: |
      ## {{ states('sensor.jf_daily_cartoon') }}
      {{ state_attr('sensor.jf_daily_cartoon', 'description') }}

      <div style="text-align: right; margin-top: 10px; font-size: 10px; opacity: 0.6; line-height: 1.6;">
        <a href="{{ state_attr('sensor.jf_daily_cartoon', 'viewer_url') }}" target="_blank" style="text-decoration: none; color: inherit;">
           ΔΕΙΤΕ ΣΕ ΠΛΗΡΕΣ ΜΕΓΕΘΟΣ
        </a>
      </div>
