# 🤣 Daily Cartoon Card για Home Assistant

Ένα απλό integration/custom sensor για το Home Assistant που φέρνει την γελοιογραφία της ημέρας απευθείας στο Lovelace Dashboard σας, προσθέτοντας μια δόση χιούμορ στην καθημερινή σας ρουτίνα.

## 🚀 Εγκατάσταση

Η κάρτα αυτή απαιτεί δύο βασικά στοιχεία:

1.  **Backend Logic (Sensor/Camera Entities):** Πρέπει να έχετε ρυθμίσει τις οντότητες `sensor.jf_daily_cartoon` και `camera.jf_daily_cartoon` (μέσω του `scrape`, `REST` ή ενός custom integration) ώστε να αντλούνται τα δεδομένα της εικόνας και του κειμένου.
2.  **Frontend Logic (Lovelace Card):** Ο παρακάτω κώδικας YAML για την εμφάνιση των δεδομένων.

## 🖼️ Lovelace YAML Configuration

Χρησιμοποιήστε τον ακόλουθο κώδικα YAML σε μία κάρτα **Manual** στο Lovelace Dashboard σας. Η διάταξη χρησιμοποιεί ένα `vertical-stack` για να συνδυάσει την εικόνα και τα συνοδευτικά στοιχεία κειμένου/συνδέσμων.

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
