import { Fragment, useContext, useEffect, useRef, useState } from "react"
import { useRouter } from "next/router"
import { Event, getAllLocalStorageItems, getRefValue, getRefValues, isTrue, preventDefault, refs, set_val, spreadArraysOrObjects, uploadFiles, useEventLoop } from "/utils/state"
import { ColorModeContext, EventLoopContext, initialEvents, StateContext } from "/utils/context.js"
import "focus-visible/dist/focus-visible"
import { Avatar, Box, Button, Container, Grid, Heading, HStack, Image, Input, Link, Modal, ModalBody, ModalContent, ModalHeader, ModalOverlay, Spacer, Text, Textarea, VStack } from "@chakra-ui/react"
import { getEventURL } from "/utils/state.js"
import { AddIcon, MoonIcon, RepeatIcon } from "@chakra-ui/icons"
import { DebounceInput } from "react-debounce-input"
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
  <VStack sx={{"width": "100%"}}>
  <Grid sx={{"gridTemplateColumns": "2fr 5fr 2fr", "width": "97%", "h": "90vh", "gap": 4}}>
  <Box sx={{"py": 4}}>
  <VStack alignItems={`left`} sx={{"gap": 4}}>
  <Container>
  <HStack>
  <MoonIcon sx={{"mr": 4, "color": "yellow", "size": "20px"}}/>
  <Text sx={{"fontSize": "40px", "fontWeight": "bolder", "fontFamily": "Calibri, Calibri", "background": "-webkit-linear-gradient(-45deg, #e04a3f, #4e8be6)", "-webkit-background-clip": "text", "color": "transparent", "centerContent": true}}>
  {`Lunar`}
</Text>
</HStack>
</Container>
  <VStack/>
  <Button onClick={(_e) => addEvents([Event("state.logout", {})], (_e), {})}>
  {`Sign out`}
</Button>
  <Container sx={{"height": "200px"}}/>
</VStack>
</Box>
  <Box sx={{"h": "100%"}}>
  <HStack justify={`space-between`} sx={{"p": 4, "borderBottom": "3px solid #000000"}}>
  <Heading size={`md`}>
  {`Story`}
</Heading>
  <Input onChange={(_e0) => addEvents([Event("state.home_state.set_search", {search:_e0.target.value})], (_e0), {})} placeholder={`Search tweets`} type={`text`}/>
</HStack>
  <VStack>
  <Container sx={{"height": "5px"}}/>
  <VStack sx={{"marginLeft": "5px", "width": "97%", "borderRadius": "20px", "border": "3px solid #000000"}}>
  <HStack sx={{"width": "95%", "marginLeft": "30px"}}>
  <Avatar size={`md`}/>
  <Container sx={{"width": "30px"}}/>
  <DebounceInput debounceTimeout={50} element={Textarea} onChange={(_e0) => addEvents([Event("state.home_state.set_tweet", {value:_e0.target.value})], (_e0), {})} placeholder={`What's happening?`} sx={{"w": "100%", "border": 2, "resize": "none", "py": 4, "px": 0, "_focus": {"border": 0, "outline": 0, "boxShadow": "none"}}} value={state.home_state.tweet}/>
</HStack>
  <HStack justifyContent={`flex-end`} sx={{"px": 4, "py": 2, "width": "100%"}}>
  <Button onClick={(_e) => addEvents([Event("state.home_state.post_tweet", {})], (_e), {})} sx={{"margin-left": "auto", "borderRadius": "1em", "boxShadow": "rgba(151, 65, 252, 0.8) 0 15px 30px -10px", "backgroundImage": "linear-gradient(144deg,#AF40FF,#5B42F3 50%,#00DDEB)", "boxSizing": "border-box", "color": "white", "opacity": "0.6", "_hover": {"opacity": 1}}}>
  {`Tweet`}
</Button>
</HStack>
</VStack>
</VStack>
  <Container sx={{"height": "10px"}}/>
  <Fragment>
  {isTrue(state.home_state.tweets) ? (
  <Fragment>
  {state.home_state.tweets.map((cwuwwhbn, mnmrfppv) => (
  <VStack alignItems={`start`} key={mnmrfppv} sx={{"marginLeft": "15px", "width": "auto"}}>
  <HStack sx={{"py": 4, "gap": 1, "border": "3px solid #3498db", "borderRadius": "10px", "width": "98%"}}>
  <Container sx={{"width": "5px"}}/>
  <VStack>
  <Avatar name={cwuwwhbn.author} size={`sm`}/>
</VStack>
  <Box sx={{"width": "100%"}}>
  <HStack>
  <Text sx={{"fontWeight": "bold"}}>
  {("@" + cwuwwhbn.author)}
</Text>
  <Text>
  {(("[" + cwuwwhbn.created_at) + "]")}
</Text>
</HStack>
  <Text sx={{"width": "100%"}}>
  {cwuwwhbn.content}
</Text>
</Box>
</HStack>
  <Container sx={{"height": "5px"}}/>
</VStack>
))}
</Fragment>
) : (
  <Fragment>
  <VStack sx={{"p": 4}}>
  <Button onClick={(_e) => addEvents([Event("state.home_state.get_tweets", {})], (_e), {})}>
  <RepeatIcon sx={{"mr": 1}}/>
  <Text>
  {`Click to load tweets`}
</Text>
</Button>
</VStack>
</Fragment>
)}
</Fragment>
</Box>
  <VStack alignItems={`start`} sx={{"gap": 4, "h": "100%", "py": 4}}>
  <Input onChange={(_e0) => addEvents([Event("state.home_state.set_friend", {value:_e0.target.value})], (_e0), {})} placeholder={`Search users`} sx={{"width": "100%", "border": "3px solid #000000"}} type={`text`}/>
  {state.home_state.search_users.map((oxensgvb, szydycsw) => (
  <VStack key={szydycsw} sx={{"py": 2, "width": "100%"}}>
  <HStack sx={{"width": "100%"}}>
  <Avatar name={oxensgvb.username} size={`sm`}/>
  <Text>
  {oxensgvb.username}
</Text>
  <Spacer/>
  <Button onClick={(_e) => addEvents([Event("state.home_state.follow_user", {username:oxensgvb.username})], (_e), {})}>
  <AddIcon/>
</Button>
</HStack>
</VStack>
))}
</VStack>
</Grid>
  <HStack>
  <Link as={NextLink} href={`/`} sx={{"display": "inline-flex", "alignItems": "center", "py": 3, "px": 6, "border": "1px solid #000000", "fontWeight": "semibold", "borderRadius": "full"}}>
  <Image src={`/Home.png`} sx={{"width": "30px", "height": "30px"}}/>
</Link>
</HStack>
</VStack>
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
