import random
from dataclasses import dataclass
from typing import List, Dict
import os
from time import sleep

@dataclass
class Protection:
    name: str
    resistance: int
    protection_type: str

@dataclass
class Disaster:
    name: str
    base_power: int
    max_power: int
    disaster_type: str
    continent: str

@dataclass
class Continent:
    name: str
    habitations: int = 0
    disasters: List[Disaster] = None
    protections: List[Protection] = None

class WeatherGame:
    def __init__(self):
        self.current_month = 1
        self.current_turn = 0  # Start at 0 so first next_turn() brings us to turn 1
        self.total_turns = 24
        
        # Initialize continents
        self.continents = {
            "Europe": Continent("Europe"),
            "Asia": Continent("Asia"),
            "Africa": Continent("Africa"),
            "North_America": Continent("North America"),
            "South_America": Continent("South America"),
            "Oceania": Continent("Oceania")
        }
        
        # Initialize disasters for each continent
        self.initialize_disasters()
        
        # Available protections
        self.protections = [
            Protection("Fondations Renforcées", 1, "earthquake"),
            Protection("Matériaux Ignifugés", 1, "fire"),
            Protection("Isolation Contre les Inondations", 2, "flood"),
            Protection("Barrière Anti-Vent", 1, "wind"),
            Protection("Revêtement Anti-Insectes", 1, "insect")
        ]

    def initialize_disasters(self):
        disasters = {
            "Europe": [
                Disaster("Inondation Européenne", 1, 4, "flood", "Europe"),
                Disaster("Tempête Hivernale", 1, 3, "wind", "Europe"),
                Disaster("Vague de Chaleur Méditerranéenne", 1, 3, "fire", "Europe"),
                Disaster("Éruption Volcanique Islandaise", 1, 5, "fire", "Europe"),
                Disaster("Séisme Méditerranéen", 1, 4, "earthquake", "Europe"),
                Disaster("Incendie de Forêt en Europe du Sud", 1, 3, "fire", "Europe"),
                Disaster("Crue Subite des Alpes", 1, 3, "flood", "Europe"),
            ],
            "Asia": [
                Disaster("Typhon Asiatique", 1, 5, "wind", "Asia"),
                Disaster("Séisme d'Himalaya", 1, 5, "earthquake", "Asia"),
                Disaster("Tsunami Pacifique", 1, 5, "flood", "Asia"),
                Disaster("Inondation de Mousson", 1, 4, "flood", "Asia"),
                Disaster("Éruption Volcanique Indonésienne", 1, 5, "fire", "Asia"),
                Disaster("Tempête de Sable Asiatique", 1, 3, "wind", "Asia"),
                Disaster("Smog Industriel", 1, 2, "other", "Asia"),
            ],
            "Africa": [
                Disaster("Sécheresse Sahélienne", 1, 5, "fire", "Africa"),
                Disaster("Inondation Tropicale", 1, 4, "flood", "Africa"),
                Disaster("Tempête de Sable Saharienne", 1, 3, "wind", "Africa"),
                Disaster("Invasion de Criquets Pèlerins", 1, 3, "insect", "Africa"),
                Disaster("Séisme de la Vallée du Rift", 1, 4, "earthquake", "Africa"),
                Disaster("Feu de Brousse en Afrique Australe", 1, 3, "fire", "Africa"),
                Disaster("Cyclone du Canal du Mozambique", 1, 5, "wind", "Africa"),
            ],
            "North_America": [
                Disaster("Ouragan Atlantique", 1, 5, "wind", "North_America"),
                Disaster("Tornade du Midwest", 1, 4, "wind", "North_America"),
                Disaster("Incendie de Forêt de Californie", 1, 4, "fire", "North_America"),
                Disaster("Séisme de la Faille de San Andreas", 1, 5, "earthquake", "North_America"),
                Disaster("Inondation du Mississippi", 1, 4, "flood", "North_America"),
                Disaster("Tempête de Neige du Nord-Est", 1, 3, "wind", "North_America"),
                Disaster("Éruption du Mont Saint Helens", 1, 5, "fire", "North_America"),
            ],
            "South_America": [
                Disaster("Inondation de l'Amazone", 1, 4, "flood", "South_America"),
                Disaster("Séisme de la Cordillère des Andes", 1, 5, "earthquake", "South_America"),
                Disaster("Éruption Volcanique Andine", 1, 4, "fire", "South_America"),
                Disaster("Glissement de Terrain Andin", 1, 3, "earthquake", "South_America"),
                Disaster("Tempête Tropicale Atlantique", 1, 3, "wind", "South_America"),
                Disaster("Sécheresse du Nordeste Brésilien", 1, 3, "fire", "South_America"),
                Disaster("Invasion de Criquets des Pampas", 1, 2, "insect", "South_America"),
            ],
            "Oceania": [
                Disaster("Cyclone du Pacifique Sud", 1, 4, "wind", "Oceania"),
                Disaster("Feu de Brousse Australien", 1, 4, "fire", "Oceania"),
                Disaster("Séisme en Nouvelle-Zélande", 1, 5, "earthquake", "Oceania"),
                Disaster("Blanchissement des Coraux", 1, 3, "other", "Oceania"),
                Disaster("Tempête de Sable du Désert Australien", 1, 2, "wind", "Oceania"),
                Disaster("Inondation Tropicale des Îles Fidji", 1, 3, "flood", "Oceania"),
                Disaster("Éruption Volcanique de Vanuatu", 1, 4, "fire", "Oceania"),
            ],
        }
        
        for continent_name, continent_disasters in disasters.items():
            self.continents[continent_name].disasters = continent_disasters

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_status(self):
        self.clear_screen()
        print(f"\n🌍 Tour {self.current_turn}/24 (Mois {self.current_month})")
        print("\nStatut des continents:")
        print("-" * 50)
        for continent in self.continents.values():
            print(f"{continent.name}: {continent.habitations} habitations")
        print("-" * 50)

    def add_habitation(self):
        """Add one habitation to each continent every other turn"""
        if self.current_turn % 2 == 0:  # Every second turn
            for continent in self.continents.values():
                continent.habitations += 1
                print(f"\n🏠 Nouvelle habitation construite en {continent.name}!")
            sleep(2)  # Give time to read the message

    def calculate_disaster_power(self, disaster: Disaster, continent: Continent) -> int:
        """Calculate the final power of a disaster including all reinforcements"""
        power = disaster.base_power
        
        # Continental Overload (bonus par tranche de 3 habitations)
        continental_bonus = continent.habitations // 3
        power += continental_bonus
            
        # Global Pressure (bonus par tranche de 10 habitations)
        total_habitations = sum(c.habitations for c in self.continents.values())
        global_bonus = total_habitations // 10
        power += global_bonus
            
        return min(power, disaster.max_power)

    def simulate_weather(self):
        """Simulate weather events for 2-3 random continents"""
        target_continents = random.sample(list(self.continents.keys()), 
                                        random.randint(2, 3))
        
        print("\n⚡ Événements météorologiques de ce tour:")
        print("-" * 50)
        
        for continent_name in target_continents:
            continent = self.continents[continent_name]
            if continent.disasters:
                disaster = random.choice(continent.disasters)
                power = self.calculate_disaster_power(disaster, continent)
                
                print(f"\n{continent.name} subit: {disaster.name}")
                print(f"Puissance: {power}")
                
        input("\nAppuyez sur Entrée pour continuer...")

    def next_turn(self):
        """Advance to the next turn"""
        self.current_turn += 1
        self.current_month = ((self.current_turn - 1) // 2) + 1
        print(f"\n=== Début du Tour {self.current_turn} (Mois {self.current_month}) ===\n")
        self.add_habitation()
        self.display_status()
        self.simulate_weather()
        
        input("\nAppuyez sur Entrée pour continuer...")

    def run(self):
        """Main game loop"""
        print("\n🎮 Bienvenue dans la simulation météorologique!")
        print("Appuyez sur Entrée pour commencer...")
        input()
        
        while self.current_turn <= self.total_turns:
            self.next_turn()
            
        print("\n🎬 Fin de la simulation!")
        print("Merci d'avoir joué!")

if __name__ == "__main__":
    game = WeatherGame()
    game.run()