from django.core.management.base import BaseCommand
from restaurants.models import District, Cuisine, Establishment, Branch, Table, WorkingHours
from django.utils import timezone
from decimal import Decimal


class Command(BaseCommand):
    help = 'Инициализация базы данных начальными данными'

    def handle(self, *args, **options):
        self.stdout.write('Начинаю инициализацию данных...')
        
        # Создание районов
        districts = [
            {"id": 1, "name": "Центральный"},
            {"id": 2, "name": "Чуркин"},
            {"id": 3, "name": "Вторая речка"},
            {"id": 4, "name": "Баляева"},
            {"id": 5, "name": "БАМ"}
        ]
        for district_data in districts:
            District.objects.get_or_create(id=district_data["id"], defaults={"name": district_data["name"]})
        self.stdout.write(self.style.SUCCESS('Районы созданы успешно'))
        
        # Создание кухонь
        cuisines = [
            {"id": 1, "name": "Русская"},
            {"id": 2, "name": "Японская"},
            {"id": 3, "name": "Итальянская"},
            {"id": 4, "name": "Грузинская"},
            {"id": 5, "name": "Корейская"},
            {"id": 6, "name": "Китайская"},
            {"id": 7, "name": "Американская"},
            {"id": 8, "name": "Европейская"},
            {"id": 9, "name": "Французская"}
        ]
        for cuisine_data in cuisines:
            Cuisine.objects.get_or_create(id=cuisine_data["id"], defaults={"name": cuisine_data["name"]})
        self.stdout.write(self.style.SUCCESS('Кухни созданы успешно'))
        
        # Создание заведений
        establishments = [
            {"id": 1, "name": "Супра", "establishment_type": "restaurant", "description": "Грузинский ресторан", "email": None, "website_url": None},
            {"id": 2, "name": "Миллионка", "establishment_type": "restaurant", "description": "Ресторан русской кухни", "email": None, "website_url": None},
            {"id": 3, "name": "IL Патио", "establishment_type": "restaurant", "description": "Итальянский ресторан", "email": None, "website_url": None},
            {"id": 4, "name": "Токио", "establishment_type": "restaurant", "description": "Японский ресторан", "email": None, "website_url": None},
            {"id": 5, "name": "Дело в мясе", "establishment_type": "restaurant", "description": "Стейк-хаус", "email": None, "website_url": None},
            {"id": 6, "name": "Studio", "establishment_type": "restaurant", "description": "Европейская кухня", "email": None, "website_url": None},
            {"id": 7, "name": "Панда", "establishment_type": "restaurant", "description": "Китайский ресторан", "email": None, "website_url": None},
            {"id": 8, "name": "GANGNAM", "establishment_type": "restaurant", "description": "Корейский ресторан", "email": None, "website_url": None},
            {"id": 9, "name": "Rakushka", "establishment_type": "restaurant", "description": "Ресторан морепродуктов", "email": None, "website_url": None},
            {"id": 10, "name": "Миринэ", "establishment_type": "restaurant", "description": "Японский ресторан", "email": None, "website_url": None},
            {"id": 11, "name": "ШашлыкоFF", "establishment_type": "restaurant", "description": "Ресторан кавказской кухни", "email": None, "website_url": None}
        ]
        
        cuisine_mappings = {
            1: [4, 1],  # Супра: Грузинская, Русская
            2: [1],     # Миллионка: Русская
            3: [3],     # IL Патио: Итальянская
            4: [2],     # Токио: Японская
            5: [7, 8],  # Дело в мясе: Американская, Европейская
            6: [8],     # Studio: Европейская
            7: [6],     # Панда: Китайская
            8: [5],     # GANGNAM: Корейская
            9: [8, 1],  # Rakushka: Европейская, Русская
            10: [2],    # Миринэ: Японская
            11: [4, 1]  # ШашлыкоFF: Грузинская, Русская
        }
        
        for est_data in establishments:
            est, created = Establishment.objects.get_or_create(id=est_data["id"], defaults=est_data)
            
            # Добавляем кухни
            cuisine_ids = cuisine_mappings.get(est_data["id"], [])
            for cuisine_id in cuisine_ids:
                cuisine = Cuisine.objects.get(id=cuisine_id)
                est.cuisines.add(cuisine)
        
        self.stdout.write(self.style.SUCCESS('Заведения созданы успешно'))
        
        # Создание филиалов
        branches = [
            {"id": 1, "establishment_id": 1, "name": "Филиал 1", "address": "ул. Светланская, 1", "district_id": 1, "phone": "2340001", "average_check": Decimal('1500.00'), "is_main": True},
            {"id": 2, "establishment_id": 2, "name": "Филиал 1", "address": "ул. Светланская, 2", "district_id": 1, "phone": "2340002", "average_check": Decimal('2000.00'), "is_main": True},
            {"id": 3, "establishment_id": 3, "name": "Филиал 1", "address": "ул. Светланская, 3", "district_id": 1, "phone": "2340003", "average_check": Decimal('1800.00'), "is_main": True},
            {"id": 4, "establishment_id": 4, "name": "Филиал 1", "address": "ул. Светланская, 4", "district_id": 1, "phone": "2340004", "average_check": Decimal('2500.00'), "is_main": True},
            {"id": 5, "establishment_id": 5, "name": "Филиал 1", "address": "ул. Светланская, 5", "district_id": 1, "phone": "2340005", "average_check": Decimal('3000.00'), "is_main": True},
            {"id": 6, "establishment_id": 6, "name": "Филиал 1", "address": "ул. Светланская, 6", "district_id": 1, "phone": "2340006", "average_check": Decimal('2200.00'), "is_main": True},
            {"id": 7, "establishment_id": 7, "name": "Филиал 1", "address": "ул. Светланская, 7", "district_id": 1, "phone": "2340007", "average_check": Decimal('1200.00'), "is_main": True},
            {"id": 8, "establishment_id": 8, "name": "Филиал 1", "address": "ул. Светланская, 8", "district_id": 1, "phone": "2340008", "average_check": Decimal('2000.00'), "is_main": True},
            {"id": 9, "establishment_id": 9, "name": "Филиал 1", "address": "ул. Светланская, 9", "district_id": 1, "phone": "2340009", "average_check": Decimal('2800.00'), "is_main": True},
            {"id": 10, "establishment_id": 10, "name": "Филиал 1", "address": "ул. Светланская, 10", "district_id": 1, "phone": "2340010", "average_check": Decimal('2000.00'), "is_main": True},
            {"id": 11, "establishment_id": 11, "name": "Филиал 1", "address": "ул. Светланская, 11", "district_id": 1, "phone": "2340011", "average_check": Decimal('1500.00'), "is_main": True}
        ]
        for branch_data in branches:
            establishment = Establishment.objects.get(id=branch_data["establishment_id"])
            district = District.objects.get(id=branch_data["district_id"])
            
            # Создаем копию данных, чтобы не изменять оригинал при pop
            branch_data_copy = branch_data.copy()
            branch_data_copy["establishment"] = establishment
            branch_data_copy["district"] = district
            branch_data_copy.pop("establishment_id")
            branch_data_copy.pop("district_id")
            
            Branch.objects.get_or_create(id=branch_data_copy["id"], defaults=branch_data_copy)
        
        self.stdout.write(self.style.SUCCESS('Филиалы созданы успешно'))
        
        # Создание столов
        tables = []
        for branch_id in range(1, 12):
            for table_number in range(1, 5):
                capacity = 6 if table_number == 3 else (2 if table_number == 4 else 4)
                tables.append({"branch_id": branch_id, "number": table_number, "capacity": capacity})
        
        for table_data in tables:
            branch = Branch.objects.get(id=table_data["branch_id"])
            table_data_copy = table_data.copy()
            table_data_copy["branch"] = branch
            table_data_copy.pop("branch_id")
            Table.objects.get_or_create(
                branch=branch, 
                number=table_data_copy["number"], 
                defaults={"capacity": table_data_copy["capacity"]}
            )
        
        self.stdout.write(self.style.SUCCESS('Столы созданы успешно'))
        
        # Создание рабочих часов
        working_hours = []
        for branch_id in range(1, 12):
            for day in range(7):
                closing_time = '23:00' if day in [5, 6] else '22:00'  # Пт и Сб до 23:00, остальные дни до 22:00
                working_hours.append({
                    "branch_id": branch_id,
                    "day_of_week": day,
                    "opening_time": "10:00",
                    "closing_time": closing_time,
                    "is_closed": False
                })
        
        for wh_data in working_hours:
            branch = Branch.objects.get(id=wh_data["branch_id"])
            wh_data_copy = wh_data.copy()
            wh_data_copy["branch"] = branch
            wh_data_copy.pop("branch_id")
            WorkingHours.objects.get_or_create(
                branch=branch, 
                day_of_week=wh_data_copy["day_of_week"], 
                defaults=wh_data_copy
            )
        
        self.stdout.write(self.style.SUCCESS('Рабочие часы созданы успешно')) 