import { StyleSheet, Text, SafeAreaView, View } from "react-native";
import { LandingPage } from "./components/LandingPage";
import { Home } from "./components/Home"
import { NavigationContainer } from "@react-navigation/native"
import { createNativeStackNavigator } from "@react-navigation/native-stack"
import { RootStackParamList } from "./RootStackParams"
import tailwind from "tailwind-rn"


const Stack = createNativeStackNavigator<RootStackParamList>()

export default function App() {
  return (
      <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen name="Login" component={LandingPage} />
        <Stack.Screen name="Home" component={Home} />
      </ Stack.Navigator>
      </ NavigationContainer>
  );
}