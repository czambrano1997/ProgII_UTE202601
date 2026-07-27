import requests

ODOO_BASE_URL = "http://localhost:8069/api_ute"

class OdooAPIService:

    @staticmethod
    def get_all(model_name):
        """Consume GET /api_ute/<model_name>/all"""
        try:
            response = requests.get(f"{ODOO_BASE_URL}/{model_name}/all", timeout=5)
            if response.status_code == 200:
                return response.json().get('data', [])
        except Exception as e:
            print(f"Error al obtener {model_name}: {e}")
        return []

    @staticmethod
    def create(model_name, payload):
        """Consume POST /api_ute/<model_name>/create"""
        try:
            response = requests.post(f"{ODOO_BASE_URL}/{model_name}/create", json=payload, timeout=5)
            return response.json()
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @staticmethod
    def delete(model_name, record_id):
        """Consume DELETE /api_ute/<model_name>/delete/<id>"""
        try:
            response = requests.delete(f"{ODOO_BASE_URL}/{model_name}/delete/{record_id}", timeout=5)
            return response.json()
        except Exception as e:
            return {'status': 'error', 'message': str(e)}