// import * as React from "react";
import { StatusBar } from "expo-status-bar";
import React, { useState, useEffect } from "react";
import { NavigationContainer, useIsFocused } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import LoginScreen from "./navigation/screens/login";
const loginName = "Login";
const Stack = createNativeStackNavigator();

function App() {
	return (
		<NavigationContainer>
			<Stack.Navigator
				screenOptions={{
					// headerTintColor: "white",
					// headerStyle: { backgroundColor: "tomato" },
					// title: "",
					// headerTransparent: true,
					headerShown: false,
				}}>
				<Stack.Screen name={loginName} component={LoginScreen} />
			</Stack.Navigator>
		</NavigationContainer>
	);
}

export default App;
