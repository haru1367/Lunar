import { Fragment, useContext, useEffect, useRef, useState } from "react"
import { useRouter } from "next/router"
import { Event, getAllLocalStorageItems, getRefValue, getRefValues, isTrue, preventDefault, refs, set_val, spreadArraysOrObjects, uploadFiles, useEventLoop } from "/utils/state"
import { ColorModeContext, EventLoopContext, initialEvents, StateContext } from "/utils/context.js"
import "focus-visible/dist/focus-visible"
import { Button, Container, FormControl, FormErrorMessage, FormHelperText, HStack, Image, Input, Link, Modal, ModalBody, ModalContent, ModalHeader, ModalOverlay, option, Select, Text, VStack } from "@chakra-ui/react"
import { getEventURL } from "/utils/state.js"
import NextLink from "next/link"
import NextHead from "next/head"



export default function Component() {
  const state = useContext(StateContext)
  const router = useRouter()
  const [ colorMode, toggleColorMode ] = useContext(ColorModeContext)
  const focusRef = useRef();
  
  // Main event loop.
  const [addEvents, connectError] = useContext(EventLoopContext)

  // Set focus to the specified element.
  useEffect(() => {
    if (focusRef.current) {
      focusRef.current.focus();
    }
  })

  // Route after the initial page hydration.
  useEffect(() => {
    const change_complete = () => addEvents(initialEvents())
    router.events.on('routeChangeComplete', change_complete)
    return () => {
      router.events.off('routeChangeComplete', change_complete)
    }
  }, [router])


  return (
    <Fragment>
  <Fragment>
  {isTrue(connectError !== null) ? (
  <Fragment>
  <Modal isOpen={connectError !== null}>
  <ModalOverlay>
  <ModalContent>
  <ModalHeader>
  {`Connection Error`}
</ModalHeader>
  <ModalBody>
  <Text>
  {`Cannot connect to server: `}
  {(connectError !== null) ? connectError.message : ''}
  {`. Check if server is reachable at `}
  {getEventURL().href}
</Text>
</ModalBody>
</ModalContent>
</ModalOverlay>
</Modal>
</Fragment>
) : (
  <Fragment/>
)}
</Fragment>
  <Container centerContent={true} sx={{"justifyContent": true, "maxWidth": "auto", "maxHeight": "auto", "height": "100vh"}}>
  <Container sx={{"height": "100px"}}/>
  <HStack>
  <VStack sx={{"width": "500px", "height": "100%"}}>
  <HStack>
  <VStack>
  <Container sx={{"height": "20px"}}/>
  <Image src={`/moonico.ico`} sx={{"width": "70px", "height": "70px"}}/>
</VStack>
  <VStack>
  <Container sx={{"height": "8px"}}/>
  <Container>
  <Text sx={{"fontSize": "50px", "fontWeight": "bolder", "letterSpacing": "3px", "fontFamily": "Comic Sans MS, Cursive", "background": "-webkit-linear-gradient(-45deg, #e04a3f, #24d6d6)", "-webkit-background-clip": "text", "color": "black", "mb": -3}}>
  {`Lunar`}
</Text>
  <Text sx={{"background": "-webkit-linear-gradient(-45deg, #e04a3f, #4e8be6)", "backgroundClip": "text", "color": "transparent", "fontWeight": "bold", "fontSize": "20px"}}>
  {`Share your daily life with people!`}
</Text>
</Container>
</VStack>
</HStack>
  <Container sx={{"height": "40px"}}/>
  <Image src={`/space2.jpg`}/>
</VStack>
  <Container sx={{"width": "30px"}}/>
  <VStack sx={{"width": "500px", "height": "auto", "centerContent": true, "borderRadius": "40px", "boxShadow": "10px 10px 100px #79d0ed", "background": "rgb(255,255,255,0.7)"}}>
  <Container sx={{"height": "20px"}}/>
  <Container sx={{"alignItems": "left", "bg": "white", "border": "1px solid #eaeaea", "p": 4, "maxWidth": "400px", "borderRadius": "lg"}}>
  <HStack>
  <Input onBlur={(_e0) => addEvents([Event("state.auth_state.set_username", {value:_e0.target.value})], (_e0), {})} placeholder={`Nickname`} type={`text`}/>
  <Button onClick={(_e) => addEvents([Event("state.auth_state.id_check", {})], (_e), {})} sx={{"bg": "#212963", "color": "white", "_hover": {"bg": "blue.600"}}}>
  {`Check`}
</Button>
</HStack>
  <Container sx={{"height": "16px"}}/>
  <FormControl isInvalid={state.auth_state.time_valid_password} isRequired={true}>
  <Input onBlur={(_e0) => addEvents([Event("state.auth_state.set_password", {value:_e0.target.value})], (_e0), {})} placeholder={`password`} type={`password`}/>
  <Fragment>
  {isTrue(state.auth_state.time_valid_password) ? (
  <Fragment>
  <FormErrorMessage>
  {`The password must be 8 to 16 characters containing a combination of numbers and alphabets.`}
</FormErrorMessage>
</Fragment>
) : (
  <Fragment>
  <FormHelperText>
  {`password is valid`}
</FormHelperText>
</Fragment>
)}
</Fragment>
</FormControl>
  <Container sx={{"height": "16px"}}/>
  <FormControl isInvalid={state.auth_state.time_valid_confirm_password} isRequired={true}>
  <Input onBlur={(_e0) => addEvents([Event("state.auth_state.set_confirm_password", {value:_e0.target.value})], (_e0), {})} placeholder={`password`} type={`password`}/>
  <Fragment>
  {isTrue(state.auth_state.time_valid_confirm_password) ? (
  <Fragment>
  <FormErrorMessage>
  {`Please check your password again.`}
</FormErrorMessage>
</Fragment>
) : (
  <Fragment>
  <FormHelperText>
  {`The passwords match.`}
</FormHelperText>
</Fragment>
)}
</Fragment>
</FormControl>
  <Container sx={{"height": "16px"}}/>
  <FormControl isInvalid={state.auth_state.time_valid_username} isRequired={true}>
  <Input onBlur={(_e0) => addEvents([Event("state.auth_state.set_user_realname", {value:_e0.target.value})], (_e0), {})} placeholder={`your name`} type={`text`}/>
  <Fragment>
  {isTrue(state.auth_state.time_valid_username) ? (
  <Fragment>
  <FormErrorMessage>
  {`The name must be between 2 and 20 characters.`}
</FormErrorMessage>
</Fragment>
) : (
  <Fragment>
  <FormHelperText>
  {`name is valid`}
</FormHelperText>
</Fragment>
)}
</Fragment>
</FormControl>
  <Container sx={{"height": "16px"}}/>
  <FormControl isInvalid={state.auth_state.time_valid_email_address} isRequired={true}>
  <Input onBlur={(_e0) => addEvents([Event("state.auth_state.set_user_email_address", {value:_e0.target.value})], (_e0), {})} placeholder={`your email address`} type={`text`}/>
  <Fragment>
  {isTrue(state.auth_state.time_valid_email_address) ? (
  <Fragment>
  <FormErrorMessage>
  {`Please enter correct email.`}
</FormErrorMessage>
</Fragment>
) : (
  <Fragment>
  <FormHelperText>
  {`check`}
</FormHelperText>
</Fragment>
)}
</Fragment>
</FormControl>
  <Container sx={{"height": "16px"}}/>
  <HStack>
  <Select onChange={(_e0) => addEvents([Event("state.auth_state.set_user_birthday_year", {value:_e0.target.value})], (_e0), {})} placeholder={`birth year`} sx={{"colorSchemes": "twitter"}}>
  {state.auth_state.year.map((smjccjab, cngauide) => (
  <option key={cngauide} value={smjccjab}>
  {smjccjab}
</option>
))}
</Select>
  <Select onChange={(_e0) => addEvents([Event("state.auth_state.set_user_birthday_month", {value:_e0.target.value})], (_e0), {})} placeholder={`birth month`} sx={{"colorSchemes": "twitter"}}>
  {state.auth_state.month.map((udiqcydy, fnozdlft) => (
  <option key={fnozdlft} value={udiqcydy}>
  {udiqcydy}
</option>
))}
</Select>
  <Select onChange={(_e0) => addEvents([Event("state.auth_state.set_user_birthday_day", {value:_e0.target.value})], (_e0), {})} placeholder={`birth day`} sx={{"colorSchemes": "twitter"}}>
  {state.auth_state.day.map((xcmhbfta, opqqvqzf) => (
  <option key={opqqvqzf} value={xcmhbfta}>
  {xcmhbfta}
</option>
))}
</Select>
</HStack>
  <VStack alignItems={`left`} sx={{"centerContent": true, "bg": "white", "maxWidth": "400px", "borderRadius": "20px", "background": "rgb(255,255,255,0.7)"}}>
  <Container sx={{"height": "20px"}}/>
  <Button onClick={(_e) => addEvents([Event("state.auth_state.signup", {})], (_e), {})} sx={{"bg": "#212963", "color": "white", "_hover": {"bg": "blue.600"}}}>
  {`Sign up`}
</Button>
</VStack>
</Container>
  <Text sx={{"color": "gray.600"}}>
  {`Already have an account? `}
  <Link as={NextLink} href={`/`} sx={{"color": "yellow.500"}}>
  {`Sign in here.`}
</Link>
</Text>
  <Container sx={{"height": "10px"}}/>
</VStack>
</HStack>
</Container>
  <NextHead>
  <title>
  {`Reflex App`}
</title>
  <meta content={`A Reflex app.`} name={`description`}/>
  <meta content={`favicon.ico`} property={`og:image`}/>
</NextHead>
</Fragment>
  )
}
