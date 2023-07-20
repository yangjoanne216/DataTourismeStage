# main.py
from PyQt5.QtWidgets import QApplication
from model import DataProcessor
from controller import ApplicationController
from view import ApplicationView

if __name__ == "__main__":
    # 需要一个QApplication实例才能运行
    app = QApplication([])

    # 初始化模型，视图，控制器
    model = DataProcessor('flux/objects/0', 'output.csv')
    # 创建和运行视图（主循环）
    etiquettes_list = [
    "Accommodation",
    "TrainingWorkshop",
    "ExecutiveBoardMeeting",
    "Store",
    "Commemoration",
    "SportsCompetition",
    "Conference",
    "Congress",
    "BoardMeeting",
    "DanceEvent",
    "ArtistSigning",
    "SportsDemonstration",
    "ChildrensEvent",
    "Exhibition",
    "Festival",
    "TastingProvider",
    "CyclingTour",
    "FluvialTour",
    "WalkingTour",
    "RoadTour",
    "UnderwaterRoute",
    "MTBRouteTheme",
    "CycleRouteTheme",
    "HorseTour",
    "Game",
    "Reading",
    "MedicalPlace",
    "Rental",
    "Practice",
    "ActivityProvider",
    "ServiceProvider",
    "AccommodationProduct",
    "Rally",
    "Rambling",
    "FoodEstablishment",
    "WorkMeeting",
    "ConvenientService",
    "CulturalSite",
    "BusinessPlace",
    "NaturalHeritage",
    "SportsAndLeisurePlace",
    "VisualArtsEvent",
    "ShowEvent",
    "CircusEvent",
    "Seminar",
    "Transport",
    "TypeOfBed",
    "Harvest",
    "Visit",
    "BusinessEvent",
    "ScaleReview",
    "BicycleLocomotionMode",
    "EquestrianLocomotionMode",
    "Tour",
    "PlaceOfInterest",
    "RouteTheme",
    "ScaleRating",
    "Organization",
    "Person",
    "GeographicReach",
    "ActivityPricingOffer",
    "RentalPricingOffer",
    "CateringPricingOffer",
    "GeneralPricingOffer",
    "Product",
    "PedestrianLocomotionMode",
    "RecurrentPeriod",
    "RoadsideLocomotionMode",
    "AdaptedsportsLocomotionMode",
    "WintersportsLocomotionMode",
    "InformativeFeatureSpecification",
    "ArchitecturalStyle",
    "ScaleReviewSystem",
    "SpatialEnvironmentTheme",
    "EntertainmentAndEventTheme",
    "ParkAndGardenTheme",
    "FoodEstablishmentTheme",
    "HealthTheme",
    "SportsTheme",
    "CuisineCategory",
    "FoodProduct",
    "CommonAmenity",
    "AccommodationAmenity",
    "CampingAndCaravanningAmenity",
    "InformativeAmenity",
    "CulturalHeritageAmenity",
    "NaturalHeritageAmenity",
    "CateringAmenity",
    "CulturalEvent",
    "SportsEvent",
    "TourGuideAgency",
    "Agent",
    "LocalAnimation",
    "AquaticLocomotionMode",
    "Audience",
    "PeopleAudience",
    "BricABrac",
    "Carnival",
    "Review",
    "LabelReview",
    "DepartementTourismCommittee",
    "RegionalTourismCommittee",
    "CulturalTheme",
    "Parade",
    "FairOrShow",
    "EntertainmentAndEvent",
    "TraditionalCelebration",
    "ProfessionalTourGuide",
    "VolunteerTourGuideOrGreeter",
    "LabelRating",
    "TourismCentre",
    "Market",
    "LocomotionMode",
    "LocalTouristOffice",
    "Organisation",
    "IncomingTravelAgency",
    "RoomAmenity",
    "PointOfInterest",
    "OpenDay",
    "PricingOffer",
    "AccommodationPricingOffer",
    "PilgrimageAndProcession",
    "Period",
    "LimitedPeriod",
    "CommonFeatureSpecification",
    "CampingAndCaravanningFeatureSpecification",
    "TastingFeatureSpecification",
    "CulturalHeritageFeatureSpecification",
    "NaturalHeritageFeatureSpecification",
    "RoomFeatureSpecification",
    "CateringFeatureSpecification",
    "AccommodationFeatureSpecification",
    "ReviewSystem",
    "LabelReviewSystem",
    "Theme",
    "Rating",
    "GarageSale",
    "TourOperatorOrTravelAgency",
    "Amenity",
    "ReligiousEvent"
]
    departements_list = [
        "Ain", "Aisne", "Allier", "Alpes-de-Haute-Provence", "Hautes-Alpes",
        "Alpes-Maritimes", "Ardèche", "Ardennes", "Ariège", "Aube",
        "Aude", "Aveyron", "Bouches-du-Rhône", "Calvados", "Cantal",
        "Charente", "Charente-Maritime", "Cher", "Corrèze", "Corse-du-Sud",
        "Haute-Corse", "Côte-d'Or", "Côtes d'Armor", "Creuse", "Dordogne",
        "Doubs", "Drôme", "Eure", "Eure-et-Loir", "Finistère", "Gard",
        "Haute-Garonne", "Gers", "Gironde", "Hérault", "Ille-et-Vilaine",
        "Indre", "Indre-et-Loire", "Isère", "Jura", "Landes", "Loir-et-Cher",
        "Loire", "Haute-Loire", "Loire-Atlantique", "Loiret", "Lot",
        "Lot-et-Garonne", "Lozère", "Maine-et-Loire", "Manche", "Marne",
        "Haute-Marne", "Mayenne", "Meurthe-et-Moselle", "Meuse", "Morbihan",
        "Moselle", "Nièvre", "Nord", "Oise", "Orne", "Pas-de-Calais",
        "Puy-de-Dôme", "Pyrénées-Atlantiques", "Hautes-Pyrénées",
        "Pyrénées-Orientales", "Bas-Rhin", "Haut-Rhin", "Rhône", "Haute-Saône",
        "Saône-et-Loire", "Sarthe", "Savoie", "Haute-Savoie", "Paris",
        "Seine-Maritime", "Seine-et-Marne", "Yvelines", "Deux-Sèvres",
        "Somme", "Tarn", "Tarn-et-Garonne", "Var", "Vaucluse", "Vendée",
        "Vienne", "Haute-Vienne", "Vosges", "Yonne", "Territoire de Belfort",
        "Essonne", "Hauts-de-Seine", "Seine-St-Denis", "Val-de-Marne",
        "Val-d'Oise", "Guadeloupe", "Martinique", "Guyane", "La Réunion",
        "Mayotte"
    ]
    etiquettes_list.sort()
    departements_list.sort()
    view = ApplicationView(None, etiquettes_list, departements_list)

    # 初始化控制器，并将 view 和 model 传入
    controller = ApplicationController(model, view)
    # 初始化控制器，并将 view 设置为刚刚创建的 ApplicationView 实例
    #controller = ApplicationController(model)
    view = ApplicationView(controller.on_submit,etiquettes_list, departements_list)


    # 现在再将 view 的 on_submit 函数设置为 controller.on_submit
    #view.on_submit = controller.on_submit

    # 更新模型的视图
    model.set_view(view)
    view.show()
    app.exec_()


