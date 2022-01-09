import { StatusBar } from "expo-status-bar";
import React, { useState, useEffect } from "react";
import { Button, Image, StyleSheet, Text, View, TextInput } from "react-native";
import routeLogin from "../Utilis";
import { BarCodeScanner } from "expo-barcode-scanner";
const cheerio = require("cheerio");

export default function SearchScreen({ navigation, route }) {
	const [hasPermission, setHasPermission] = useState(null);
	const [scanned, setScanned] = useState(false);
	const [result, setResult] = useState("");

	// textField
	const [renderTextfield, setRenderTextField] = useState(false);
	const [textField, onChangeTextField] = useState("");

	// Text recognition
	const [renderOCR, setRenderOCR] = useState(false);

	const askForCameraPermission = () => {
		(async () => {
			const { status } = await BarCodeScanner.requestPermissionsAsync();
			setHasPermission(status == "granted"); // True given the following condition
		})();
		// ^ empty parentesis makes it a 'promise'
	};

	// Request for camera permission
	useEffect(() => {
		askForCameraPermission();
	}, []);

	// Check permissions and return the screens
	if (hasPermission === null) {
		return (
			<View style={styles.container}>
				<Text style={styles.whiteText}>Requesting for camera permission</Text>
			</View>
		);
	}

	if (hasPermission === false) {
		return (
			<View style={styles.container}>
				<Text style={(styles.whiteText, { margin: 10 })}>No access to camera</Text>
				<Button
					title={"Allow Camera"}
					onPress={() => {
						askForCameraPermission();
					}}></Button>
			</View>
		);
	}

	// What happens when we scan the bar code
	const handleBarCodeScanned = async ({ type, data }) => {
		setResult("Fetching product details..");
		onChangeTextField("Fetching product details..");
		setScanned(true);
		var product = await retrieveBarcodeTitle(data);
		console.log("Type " + type + "\nData: " + data + "\nProduct: " + product);
		product == undefined ? setResult("Item not found in database.") : setResult(product);
		product == undefined ? onChangeTextField("") : onChangeTextField(product);

		// if (product) {
		// 	const requestOptions = {
		// 		method: "POST",
		// 		headers: { "Content-Type": "application/json" },
		// 		body: JSON.stringify({
		// 			title: product,
		// 		}),
		// 	};
		// 	fetch(
		// 		"http://116.88.104.224:8000/api/perish_create_test",
		// 		requestOptions
		// 	)
		// 		.then((response) => {
		// 			response.json().then((data) => {
		// 				if (response.ok) {
		// 					console.log("response ok");
		// 				} else {
		// 					console.log("response !ok");
		// 					setResult({ error: data["Bad request"] });
		// 				}
		// 			});
		// 		})
		// 		.catch((error) => {
		// 			console.log(error);
		// 		});
		// }
	};

	// Web scraping / parsing
	async function retrieveBarcodeTitle(code) {
		var searchUrl = `https://world.openfoodfacts.org/product/${code}`;
		var response = await fetch(searchUrl); // fetch page
		var htmlString = await response.text(); // get response text
		var $ = cheerio.load(htmlString); // parse HTML string
		return $("h1[property=food:name]").text().trim();
	}

	function handleRenderTextfield() {
		return (
			<TextInput
				style={styles.input}
				onChangeText={onChangeTextField}
				value={textField}
				placeholder="Product title"
			/>
		);
	}

	function handleRenderBarcodeScan() {
		return (
			<View style={styles.container}>
				<Text style={Object.assign({}, styles.whiteText, styles.mainText)}>Scan Product Barcode</Text>
				<View style={styles.barcodebox}>
					<BarCodeScanner
						onBarCodeScanned={scanned ? undefined : handleBarCodeScanned}
						style={{ height: 600, width: "100%" }}
					/>
				</View>
				<TextInput
					style={styles.input}
					onChangeText={(change) => {
						onChangeTextField(change);
						// console.log(change);
					}}
					value={textField}
					placeholder="Click here to manually enter product title"
					placeholderTextColor="white"
				/>
				<View style={styles.options}>
					<View style={styles.button}>
						<Button
							title={"  <  "}
							onPress={() => {
								setRenderOCR(false);
								setScanned(false);
								setResult("");
								onChangeTextField("");
							}}
							color="tomato"
						/>
					</View>
					{scanned && <Button title={"Scan again?"} onPress={() => setScanned(false)} />}
					<View style={styles.button}>
						<Button title={"  >  "} onPress={() => setRenderOCR(true)} color="tomato" />
					</View>
					{/* <View style={styles.button}>
				{renderTextfield ? (
					handleTextfield()
				) : (
					<Button title={"Manually Enter title"} onPress={() => setRenderTextField(true)} color="tomato" />
				)}
			</View> */}
				</View>
			</View>
		);
	}

	function handleRenderOCR() {
		return (
			<View style={styles.container}>
				<Text style={styles.title}>OCR expiry date</Text>
				<Text style={styles.instructions}>Select an image source:</Text>
				<View style={styles.options}>
					<View style={styles.button}>
						<Button title={"  <  "} onPress={() => setRenderOCR(false)} color="tomato" />
					</View>
					<View style={styles.button}>
						<Button
							// disabled={isLoading}
							title="Camera"
							onPress={() => {
								// recognizeFromCamera();
							}}
						/>
					</View>
					<View style={styles.button}>
						<Button
							// disabled={isLoading}
							title="Picker"
							onPress={() => {
								// recognizeFromPicker();
								setLogin(false);
							}}
						/>
					</View>
				</View>
				{
					<View style={styles.imageContainer}>
						{/* <Image style={styles.image} source={imgSrc} /> */}
						{/* {isLoading ? <ProgressCircle showsText progress={progress} /> : <Text>{text}</Text>} */}
					</View>
				}
			</View>
		);
	}

	return (
		// <View style={{ flex: 1, alignItems: "center", justifyContent: "center" }}>
		// <Image style={{ height: "100%", width: "100%" }} source={require("../../assets/images/photo1.png")}></Image>
		// </View>
		renderOCR ? handleRenderOCR() : handleRenderBarcodeScan()
	);
}

const styles = StyleSheet.create({
	container: {
		flex: 1,
		backgroundColor: "#272927",
		color: "#ffffff",
		alignItems: "center",
		justifyContent: "center",
	},
	barcodebox: {
		backgroundColor: "white",
		alignItems: "center",
		justifyContent: "center",
		height: 300,
		width: 300,
		overflow: "hidden",
		borderRadius: 30,
	},
	mainText: {
		fontSize: 25,
		margin: 20,
	},
	whiteText: {
		color: "#ffffff",
	},
	button: {
		marginHorizontal: 10,
		marginVertical: 1,
	},
	input: {
		height: 40,
		margin: 12,
		borderWidth: 1,
		padding: 10,
		color: "#ffffff",
		fontSize: 16,
		margin: 20, // backgroundColor: "white",
	},
	options: {
		flexDirection: "row",
		justifyContent: "space-between",
		padding: 10,
	},
	imageContainer: {
		justifyContent: "center",
		alignItems: "center",
	},
	image: {
		marginVertical: 15,
		// height: DEFAULT_HEIGHT / 2.5,
		// width: DEFAULT_WIDTH / 2.5,
	},
	title: {
		fontSize: 20,
		textAlign: "center",
		color: "white",
		margin: 10,
	},
	instructions: {
		textAlign: "center",
		color: "white",
		marginBottom: 5,
	},
});
