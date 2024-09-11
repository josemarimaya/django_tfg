from models import Provinces

def run():
    provinces = [
        "Álava", "Albacete", "Alicante", "Almería", "Asturias", "Ávila", 
        "Badajoz", "Baleares", "Barcelona", "Burgos", "Cáceres", "Cádiz", 
        "Cantabria", "Castellón", "Ceuta", "Ciudad Real", "Córdoba", 
        "Cuenca", "Girona", "Granada", "Guadalajara", "Guipúzcoa", 
        "Huelva", "Huesca", "Jaén", "La Coruña", "La Rioja", "Las Palmas", 
        "León", "Lérida", "Lugo", "Madrid", "Málaga", "Melilla", 
        "Murcia", "Navarra", "Orense", "Palencia", "Pontevedra", "Salamanca", 
        "Segovia", "Sevilla", "Soria", "Tarragona", "Tenerife", "Teruel", 
        "Toledo", "Valencia", "Valladolid", "Vizcaya", "Zamora", "Zaragoza"
    ]

    for province in provinces:
        Provinces.objects.get_or_create(name=province)

    print(f"Se han insertado {len(provinces)} provincias.")
