import "expo-dev-client";
import React, { useEffect, useState } from "react";
import { Button, Image, StyleSheet, Text, View } from "react-native";
import ProgressCircle from "react-native-progress/Circle";
import MlkitOcr from "react-native-mlkit-ocr";
import ImagePicker from "react-native-image-crop-picker";

const DEFAULT_HEIGHT = 500;
const DEFAULT_WIDTH = 600;
const defaultPickerOptions = {
	// cropping: true,
	// height: DEFAULT_HEIGHT,
	// width: DEFAULT_WIDTH,
};

export default function App() {
	const [isLoading, setIsLoading] = useState(false);
	const [progress, setProgress] = useState(0);
	const [imgSrc, setImgSrc] = useState(null);
	const [text, setText] = useState("");

	useEffect(() => {}, []);

	const recognizeTextFromImage = async (path) => {
		setIsLoading(true);
		try {
			const recognizedText = await MlkitOcr.detectFromFile(path);
			// console.log(recognizedText);
			let recognizedNumbers = [];
			recognizedText.forEach((e) => {
				let RecognizedDate = false;
				let OCRText = e.text;
				OCRText = OCRText.replace(/[Oo]/g, "0");
				OCRText = OCRText.replace(/[\D]/g, " ");
				OCRText = OCRText.split(" ")
					.filter(Number)
					.filter((n) => (n.length == 2 && Number(n) < 32) || n.length == 4);
				if (RecognizedDate) {
					return;
				}
				// console.log(`${OCRText}\n`);
				recognizedNumbers = recognizedNumbers.concat(OCRText);
			});
			console.log(`recognizedNumbers`, recognizedNumbers);
			let recognizedYearIndex = [];
			// index of Year = int value of recognizedYear
			for (let i = 0; i < recognizedNumbers.length; i++) {
				let e = recognizedNumbers[i];
				(e.length == 4 && e.substring(0, 2) == "20") ||
				(e.length == 2 && e.substring(0, 1) == "2" && parseInt(e.substring(1, 2)) > 1)
					? recognizedYearIndex.push(recognizedNumbers.indexOf(e))
					: recognizedYearIndex;
			}
			console.log(`recognizedYearIndex = ${recognizedYearIndex}`);
			// Identifying possible index of dates
			// XX XX YYYY, YYYY XX XX, YYYY ABC XX
			// TODO: Identify printed alphabetical Months
			// TODO: Formats like 07/21 or 07/22, or 07/2X (no day)
			var numbersBehindYear = false;
			var numbersInfrontYear = false;
			var expiryDates = recognizedYearIndex.length ? "" : "No expiry date found.";

			recognizedYearIndex.forEach((i) => {
				numbersBehindYear = recognizedNumbers.length >= i + 2 ? true : false;
				numbersInfrontYear = i > 0 ? true : false;

				var e = recognizedNumbers;
				var Year = e[i];
				let fourDigitYear = Year.length == 4 ? true : false;

				// No numbers infront of year
				if (!numbersInfrontYear) {
					// expiryDates = "No expiry date found";
					return;
				} else if (numbersBehindYear) {
					expiryDates += `\IF\n`;
					if (fourDigitYear) {
						var hasLead = e[i - 2] && e[i - 2].length == 2 ? e[i - 2] : false;
						var hasTrail = e[i + 2] && e[i - 2].length == 2 ? e[i + 2] : false;
						var validLeadingMiddle = e[i - 1].length == 2 ? true : false;
						var validTrailingMiddle = e[i + 1].length == 2 ? true : false;
						hasLead && validLeadingMiddle ? (expiryDates += `${e[i - 2]}-${e[i - 1]}-${Year}\n`) : null;
						hasTrail && validTrailingMiddle ? (expiryDates += `${Year}-${e[i + 1]}-${e[i + 2]}\n`) : null;
					} else {
						expiryDates += `${e[i - 1]}/${Year}\n`;
					}
					//
				} else {
					expiryDates += `\ELSE\n`;
					if (fourDigitYear) {
						var validMiddle = e[i - 1].length == 2 || e[i + 1].length == 2 ? true : false;
						var hasLead = e[i - 2] && e[i - 2].length == 2 ? e[i - 2] : false;
						hasLead && validMiddle ? (expiryDates += `${e[i - 2]}-${e[i - 1]}-${Year}\n`) : null;
					} else {
						var validMiddle = e[i - 1].length == 2 || e[i + 1].length == 2 ? true : false;
						validMiddle ? (expiryDates += `${e[i - 1]}/${Year}\n`) : null;
					}
				}
			});

			expiryDates = !expiryDates ? "No expiry date found." : expiryDates;
			setText(expiryDates);
		} catch (err) {
			console.error(err);
			setText("");
		}
		setIsLoading(false);
	};

	const recognizeFromPicker = async (options = defaultPickerOptions) => {
		try {
			const image = await ImagePicker.openPicker(options);
			setImgSrc({ uri: image.path });
			await recognizeTextFromImage(image.path);
		} catch (err) {
			if (err.message !== "User cancelled image selection") {
				console.error(err);
			}
		}
	};

	const recognizeFromCamera = async (options = defaultPickerOptions) => {
		try {
			const image = await ImagePicker.openCamera(options);
			setImgSrc({ uri: image.path });
			await recognizeTextFromImage(image.path);
		} catch (err) {
			if (err.message !== "User cancelled image selection") {
				console.error(err);
			}
		}
	};

	return (
		<View style={styles.container}>
			<Text style={styles.title}>MLKit OCR</Text>
			<Text style={styles.instructions}>Select an image source:</Text>
			<View style={styles.options}>
				<View style={styles.button}>
					<Button
						disabled={isLoading}
						title="Camera"
						onPress={() => {
							recognizeFromCamera();
						}}
					/>
				</View>
				<View style={styles.button}>
					<Button
						disabled={isLoading}
						title="Picker"
						onPress={() => {
							recognizeFromPicker();
						}}
					/>
				</View>
			</View>
			{
				<View style={styles.imageContainer}>
					<Image style={styles.image} source={imgSrc} />
					{isLoading ? <ProgressCircle showsText progress={progress} /> : <Text>{text}</Text>}
				</View>
			}
		</View>
	);
}

const styles = StyleSheet.create({
	container: {
		flex: 1,
		justifyContent: "center",
		alignItems: "center",
		backgroundColor: "#F5FCFF",
	},
	options: {
		flexDirection: "row",
		justifyContent: "space-between",
		padding: 10,
	},
	button: {
		marginHorizontal: 10,
	},
	imageContainer: {
		justifyContent: "center",
		alignItems: "center",
	},
	image: {
		marginVertical: 15,
		height: DEFAULT_HEIGHT / 2.5,
		width: DEFAULT_WIDTH / 2.5,
	},
	title: {
		fontSize: 20,
		textAlign: "center",
		margin: 10,
	},
	instructions: {
		textAlign: "center",
		color: "#333333",
		marginBottom: 5,
	},
});
