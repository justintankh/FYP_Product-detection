import { Button, Image, StyleSheet, Text, View, TextInput, ImageBackground } from "react-native";
import LoginScreen from "./screens/login";

export default function routeLogin() {
	fetch("http://116.88.104.224:8000/api/utilis/retrieve_username").then((response) => {
		if (!response.ok) {
			console.log("not ok");
			return true;
		} else {
			return false;
		}
	});
}
