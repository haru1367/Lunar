import { Fragment, useContext, useEffect, useRef, useState } from "react"
import { useRouter } from "next/router"
import { Event, getAllLocalStorageItems, getRefValue, getRefValues, isTrue, preventDefault, refs, set_val, spreadArraysOrObjects, uploadFiles, useEventLoop } from "/utils/state"
import { ColorModeContext, EventLoopContext, initialEvents, StateContext } from "/utils/context.js"
import "focus-visible/dist/focus-visible"
import { Button, Container, HStack, Image, Input, Link, Modal, ModalBody, ModalContent, ModalHeader, ModalOverlay, Text, VStack } from "@chakra-ui/react"
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
  <Container centerContent={true} sx={{"background-image": "url('/space.jpg')", "background-size": "cover", "maxWidth": "auto", "maxHeight": "auto", "height": "100vh"}}>
  <Container sx={{"height": "150px"}}/>
  <VStack sx={{"width": "600px", "height": "auto", "centerContent": true, "borderRadius": "40px", "boxShadow": "10px 10px 100px #79d0ed", "background": "rgb(255,255,255,0.7)"}}>
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
  <Container sx={{"height": "20px"}}/>
  <Container>
  <VStack>
  <Container centerContent={true} sx={{"alignItems": "left", "bg": "white", "border": "1px solid #eaeaea", "p": 4, "maxWidth": "400px", "borderRadius": "20px", "background": "rgb(255,255,255,0.7)"}}>
  <Input onBlur={(_e0) => addEvents([Event("state.auth_state.set_username", {value:_e0.target.value})], (_e0), {})} placeholder={`Username`} sx={{"mb": 4}} type={`text`}/>
  <Input onBlur={(_e0) => addEvents([Event("state.auth_state.set_password", {value:_e0.target.value})], (_e0), {})} placeholder={`Password`} sx={{"mb": 4}} type={`password`}/>
  <Button onClick={(_e) => addEvents([Event("state.auth_state.login", {})], (_e), {})} sx={{"bg": "#212963", "color": "white", "_hover": {"bg": "blue.600"}}}>
  {`Log in`}
</Button>
</Container>
  <Container sx={{"height": "10px"}}/>
  <Text sx={{"color": "gray.600"}}>
  {`Forgot your password?   `}
  <Link as={NextLink} href={`/findpassword`} sx={{"color": "green.500"}}>
  {`Find Password!`}
</Link>
</Text>
  <Text sx={{"color": "gray.600"}}>
  {`Don't have an account yet?   `}
  <Link as={NextLink} href={`/signup`} sx={{"color": "blue.500"}}>
  {`Sign up!`}
</Link>
</Text>
  <Container sx={{"height": "30px"}}/>
</VStack>
</Container>
</VStack>
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
