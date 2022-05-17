// IMPORTS
import {
  TouchableOpacity,
  TextInput,
  View,
  ScrollView,
  StyleSheet,
  SafeAreaView,
  Text,
} from 'react-native'
import { colors, randomColor } from '../assets/colors'
import { RootStackParamList, Course } from '../RootStackParams'
import { NativeStackNavigationProp } from '@react-navigation/native-stack'
import { useNavigation } from '@react-navigation/native'
import { useState } from 'react'
import { Icon } from 'react-native-elements'
import fuzzysort from 'fuzzysort'
import React from 'react'

interface Props {
  route: { params: { profName: string; courses: Course[] } }
}

type professorScreenProp = NativeStackNavigationProp<
  RootStackParamList,
  'Professor'
>

export function Professor(Props: Props) {
  // sort all of professor courses
  const allCourses = Array.from([
    ...new Set(
      Props.route.params.courses.map((obj) => {
        return obj.course
      })
    ),
  ]).sort()

  // SET STATES
  const [wordEntered, setWordEntered] = useState('')
  const [searchBG, setSearchBG] = useState(colors.PURPLE)
  const [courses, setCourses] = useState(allCourses)

  const navigation = useNavigation<professorScreenProp>()

  // FZF String match
  // handleSearch - Params(search:string, course:string[], setCourses:function)
  function handleSearch(search: string, courses: string[], setCourses: any) {
    setCourses(
      search.length === 0
        ? allCourses
        : fuzzysort.go(search, courses).map((item) => {
            return item.target
          })
    )
  }

  return (
    <SafeAreaView style={styles.container}>
      <View>
        {/*HEADERS*/}
        <Text style={[styles.title, { paddingHorizontal: 10 }]}>
          {Props.route.params.profName}
        </Text>
        <View
          style={{
            borderTopWidth: 1,
            borderColor: colors.GRAY,
            opacity: 0.7,
            paddingVertical: 6,
          }}
        >
          <Text style={styles.departmentTitle}>Courses</Text>
        </View>

        {/*SEARCH*/}
        <View style={{ width: '90%', marginLeft: 15, marginTop: 5 }}>
          <View
            style={{
              flexDirection: 'row',
              width: '100%',
              alignItems: 'center',
              paddingBottom: 10,
            }}
          >
            <Icon
              name="search"
              style={{ opacity: 0.7 }}
              tvParallaxProperties={null}
            />
            <TextInput
              onChangeText={(word) => {
                setWordEntered(word)
                handleSearch(word, courses, setCourses)
              }}
              onFocus={() => setSearchBG(colors.GREEN)}
              onBlur={() => setSearchBG(colors.PURPLE)}
              value={wordEntered}
              clearTextOnFocus={true}
              placeholder="search for course"
              style={[
                styles.inputStyles,
                { borderColor: searchBG, flex: 5, marginLeft: -30 },
              ]}
            />
          </View>
        </View>

        {/*COURSE LIST*/}
        <ScrollView style={styles.departments}>
          {courses.map((course) => {
            return (
              <TouchableOpacity
                style={[
                  styles.departmentContainer,
                  { shadowColor: randomColor() },
                ]}
                onPress={() => {
                  navigation.navigate('Course', {
                    course: course,
                    prof: Props.route.params.profName,
                  })
                }}
                key={undefined}
              >
                <Text style={styles.department}>
                  {course.substring(0, 4)}
                  <Text
                    style={{
                      color: 'white',
                      opacity: 0.8,
                      fontWeight: '300',
                      /*(parseFloat(value.overallGPA) > 3.4) ? colors.BLUE
                : (parseFloat(value.overallGPA) > 2.8) ? colors.GREEN 
                : (parseFloat(value.overallGPA)> 2.0) ? colors.ORANGE 
                : colors.RED*/
                    }}
                  >
                    {course.substring(4, course.length)}
                  </Text>
                </Text>
              </TouchableOpacity>
            )
          })}
        </ScrollView>
      </View>
    </SafeAreaView>
  )
}

// STYLES
const styles = StyleSheet.create({
  container: {
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    marginHorizontal: 'auto',
    height: '88%',
  },
  title: {
    textAlign: 'center',
    fontSize: 40,
    marginTop: 1,
    marginBottom: 5,
    paddingHorizontal: 10,
  },
  departmentTitle: {
    fontSize: 30,
    paddingHorizontal: 30,
    textAlign: 'center',
  },
  departmentContainer: {
    backgroundColor: colors.GREEN,
    borderRadius: 30,
    marginHorizontal: 30,
    marginVertical: 10,
    shadowOffset: { width: 3, height: 2 },
    shadowOpacity: 1,
    shadowRadius: 0,
  },
  department: {
    fontSize: 40,
    textAlign: 'center',
    color: 'white',
    fontWeight: '500',
    letterSpacing: 5,
    paddingVertical: 15,
    paddingHorizontal: 40,
  },
  departments: {
    // flex: 6,
    // justifyContent: 'flex-start',
    // paddingBottom: 100,
    // height: '80%',
  },
  inputStyles: {
    borderWidth: 2,
    borderRadius: 5,
    padding: 5,
    paddingLeft: 30,
    fontSize: 15,
  },
})
