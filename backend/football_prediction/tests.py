from django.test import TestCase
import pprint


class InferencePipelineTestCases(TestCase):
    def test_successful_inference(self):
        data = {
            "home_player_01": "Alisson",
            "home_player_01_position": "GK",
            "home_player_02": "Trent Alexander-Arnold",
            "home_player_02_position": "RB",
            "home_player_03": "Andrew Robertson",
            "home_player_03_position": "LB",
            "home_player_04": "Virgil van Dijk",
            "home_player_04_position": "CB",
            "home_player_05": "Ibrahima Konaté",
            "home_player_05_position": "CB",
            "home_player_06": "Fabinho",
            "home_player_06_position": "DM",
            "home_player_07": "Thiago Alcántara",
            "home_player_07_position": "CM",
            "home_player_08": "Jordan Henderson",
            "home_player_08_position": "CM",
            "home_player_09": "Darwin Núñez",
            "home_player_09_position": "LW",
            "home_player_10": "Mohamed Salah",
            "home_player_10_position": "RW",
            "home_player_11": "Cody Gakpo",
            "home_player_11_position": "FW",
            "away_player_01": "Aaron Ramsdale",
            "away_player_01_position": "GK",
            "away_player_02": "Ben White",
            "away_player_02_position": "RB",
            "away_player_03": "Oleksandr Zinchenko",
            "away_player_03_position": "LB",
            "away_player_04": "Rob Holding",
            "away_player_04_position": "CB",
            "away_player_05": "Gabriel Dos Santos",
            "away_player_05_position": "CB",
            "away_player_06": "Thomas Partey",
            "away_player_06_position": "DM",
            "away_player_07": "Granit Xhaka",
            "away_player_07_position": "CM",
            "away_player_08": "Martin Ødegaard",
            "away_player_08_position": "CM",
            "away_player_09": "Martinelli",
            "away_player_09_position": "LW",
            "away_player_10": "Bukayo Saka",
            "away_player_10_position": "RW",
            "away_player_11": "Gabriel Jesus",
            "away_player_11_position": "FW",
        }
        response = self.client.post("/api/predict/", data=data)
        response_data = response.data
        self.assertIsInstance(response_data["home_score_pred"], float)
        self.assertIsInstance(response_data["away_score_pred"], float)
        self.assertIsInstance(response_data["home_result_pred"], str)
        
    def test_failed_inference_because_players_not_found(self):
        not_in_database_data = {
            "home_player_01": "AlissonA",
            "home_player_01_position": "GK",
            "home_player_02": "Trent Alexander-Arnold",
            "home_player_02_position": "RB",
            "home_player_03": "Andrew Robertson",
            "home_player_03_position": "LB",
            "home_player_04": "Virgil van Dijk",
            "home_player_04_position": "CB",
            "home_player_05": "Ibrahima Konaté",
            "home_player_05_position": "CB",
            "home_player_06": "Fabinho",
            "home_player_06_position": "DM",
            "home_player_07": "Thiago Alcántara",
            "home_player_07_position": "CM",
            "home_player_08": "Jordan Henderson",
            "home_player_08_position": "CM",
            "home_player_09": "Darwin Núñez",
            "home_player_09_position": "LW",
            "home_player_10": "Mohamed Salah",
            "home_player_10_position": "RW",
            "home_player_11": "Cody GakpoS",
            "home_player_11_position": "FW",
            "away_player_01": "Aaron Ramsdale",
            "away_player_01_position": "GK",
            "away_player_02": "Ben White",
            "away_player_02_position": "RB",
            "away_player_03": "Oleksandr Zinchenko",
            "away_player_03_position": "LB",
            "away_player_04": "Rob Holding",
            "away_player_04_position": "CB",
            "away_player_05": "Gabriel Dos Santos",
            "away_player_05_position": "CB",
            "away_player_06": "Thomas Partey",
            "away_player_06_position": "DM",
            "away_player_07": "Granit Xhaka",
            "away_player_07_position": "CM",
            "away_player_08": "Ø",
            "away_player_08_position": "CM",
            "away_player_09": "Martineli",
            "away_player_09_position": "LW",
            "away_player_10": "Bukayo Saka",
            "away_player_10_position": "RW",
            "away_player_11": "Gabriel Jesus",
            "away_player_11_position": "FW",
        }
        not_in_database_players = ["AlissonA", "Cody GakpoS", "Ø", "Martineli"]
        response = self.client.post("/api/predict/", data=not_in_database_data)
        response_data = response.data
        self.assertEqual(response_data["players_not_found"], not_in_database_players)