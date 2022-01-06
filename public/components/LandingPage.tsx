import { StyleSheet, SafeAreaView, Text, TextInput, View, Pressable, TouchableOpacity }  from "react-native";
import tailwind from "tailwind-rn";
import { useState } from "react"
import { NavigationContainer, useNavigation, RouteProp} from '@react-navigation/native';
import { createNativeStackNavigator, NativeStackNavigationProp } from '@react-navigation/native-stack';
import { RootStackParamList } from "../RootStackParams"

type loginScreenProp = NativeStackNavigationProp<RootStackParamList, "Login">
async function loginAPI(username:string, password:string){
  return await fetch(`http://localhost:8080/login?username=${username}&password=${password}`)
    .then(response => {
        console.log(response.status)
        if(response.status === 200) return true
        else return false
    })
    //.then(data => {return true})
    .catch(err => {
      console.error(err)
      return false 
    })  
}

export function LandingPage(){

  const [username, setUsername] = useState("username")
  const [password, setPassword] = useState("password")
  const [usernameBG, setUsernameBG] = useState("rgba(150, 150, 150, .5)")
  const [passwordBG, setPasswordBG] = useState("rgba(150, 150, 150, .5)")
  const [badLogin, setBadLogin] = useState(false)
  
  const navigation = useNavigation<loginScreenProp>()
  return (
    <SafeAreaView
      style={tailwind("w-full h-full flex-1 justify-center items-center")}
    >
      <View style={styles.titleBorderStyles}>
         <Text
          style={styles.titleStyles}
        >
          Profesi
        </Text>
      </View>
      <View style={{"width": "55%"}}>
        <TextInput
          onChangeText={setUsername}
          autoCapitalize="none"
          onFocus={() => setUsernameBG("#10b981")}
          onBlur={() => setUsernameBG("rgba(150, 150, 150, .5)")}
          value={username}
          clearTextOnFocus={true}
          defaultValue="username"
          style={[styles.inputStyles, {"marginBottom": 6, borderColor: usernameBG}]}
        />
        <TextInput
          onChangeText={setPassword}
          autoCapitalize="none"
          clearTextOnFocus={true}
          onFocus={() => setPasswordBG("#10b981")}
          onBlur={() => setPasswordBG("rgba(150, 150, 150, .5)")}
          style={[styles.inputStyles, {"marginBottom": 6, borderColor: passwordBG}]}
          value={password}
          defaultValue="password"
          secureTextEntry={password === "password" ? false : true}
        />
        <View style={{flexDirection: "column", height: "25%"}}>
          {badLogin ? 
            <Text style={styles.incorrectLoginStyles}>
              Incorrect login 
            </ Text> : null 
          }
          <TouchableOpacity 
            style={{flex: 1}}
            onPress={() => console.log("USER FORGOT PASSWORD")}
          >
            <Text style={[styles.forgotPasswordStyles, {paddingTop: badLogin ? 4 : 8}]}>
             Forgot Password? 
            </ Text>
          </ TouchableOpacity>

          <TouchableOpacity 
            style={{flex: 1}}
            onPress={() => navigation.navigate("Home")}
          >
            <Text style={styles.signupPasswordStyles}>
              Don't have an account?
            </ Text>
          </ TouchableOpacity>
          
        </ View>
        <TouchableOpacity 
          style={{borderColor: "black", width: "100%", borderWidth: 2, borderRadius: 20,}}
          onPress={() => {
            console.log("USER LOGIN: " + username + ", " + password)
            loginAPI(username,password).then(data => {
                setBadLogin(!data) 
                return data ? navigation.navigate("Home") : null
          })}}
        >
            <Text style={styles.loginStyles}>
              Login
            </ Text>
          </ TouchableOpacity>
      </View>
    </SafeAreaView>
  );
};


const styles = StyleSheet.create({
  
  titleStyles:{
    color: "black",
    fontSize: 60,
  },
  titleBorderStyles:{
    borderBottomWidth: 2,
    borderBottomColor: "orange",
    marginBottom: "3%",
    paddingRight: "8%",
    paddingLeft: "8%",
    paddingBottom: "-0%"
  },
  inputStyles:{
    borderWidth: 2,
    borderRadius: 5,
    //borderColor: "rgba(150, 150, 150, .5)",
    padding: 5,
    paddingLeft: 5,
    fontSize: 15
  },
  incorrectLoginStyles:{
    textAlign: "center",
    padding: 4,
    paddingTop: 4,
    color: "red",
    fontStyle: "italic"
  },
  forgotPasswordStyles:{
    textAlign: "center",
    padding: 4,
  },
  signupPasswordStyles:{
    textAlign: "center",
    padding: 2,
    color: "orange",
  },
  loginStyles:{
    color: "black",
    fontSize: 40,
    textAlign: "center",
    paddingTop: 8,
    paddingBottom: 8,
    fontWeight: "300",
    letterSpacing: 5
  },
})
