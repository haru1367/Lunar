import { Fragment, useContext, useEffect, useRef, useState } from "react"
import { useRouter } from "next/router"
import { Event, getAllLocalStorageItems, getRefValue, getRefValues, isTrue, preventDefault, refs, set_val, spreadArraysOrObjects, uploadFiles, useEventLoop } from "/utils/state"
import { ColorModeContext, EventLoopContext, initialEvents, StateContext } from "/utils/context.js"
import "focus-visible/dist/focus-visible"
import { Avatar, Box, Button, Grid, Heading, HStack, Input, Link, Modal, ModalBody, ModalContent, ModalHeader, ModalOverlay, Spacer, Text, Textarea, VStack } from "@chakra-ui/react"
import { getEventURL } from "/utils/state.js"
import NextLink from "next/link"
import { AddIcon, RepeatIcon, StarIcon } from "@chakra-ui/icons"
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
  <Box sx={{"width": "100%", "maxWidth": "1300px", "bg": "white", "h": "100%", "px": [4, 12], "margin": "0 auto", "position": "relative"}}>
  <Grid sx={{"gridTemplateColumns": "1fr 2fr 1fr", "h": "100vh", "gap": 4}}>
  <Box sx={{"py": 4}}>
  <VStack alignItems={`left`} sx={{"gap": 4}}>
  <Heading size={`md`}>
  {`PySocial`}
</Heading>
  <Link as={NextLink} href={`/`} sx={{"display": "inline-flex", "alignItems": "center", "py": 3, "px": 6, "border": "1px solid #eaeaea", "fontWeight": "semibold", "borderRadius": "full"}}>
  <StarIcon sx={{"mr": 2}}/>
  {`Home`}
</Link>
  <Box sx={{"p": 4, "borderRadius": "md", "border": "1px solid #eaeaea"}}>
  <Heading size={`sm`}>
  {`Followers`}
</Heading>
  {state.home_state.followers.map((gnuxevhc, olaorlcy) => (
  <VStack key={olaorlcy} sx={{"padding": "1em"}}>
  <HStack>
  <Avatar name={gnuxevhc.follower_username} size={`sm`}/>
  <Text>
  {gnuxevhc.follower_username}
</Text>
</HStack>
</VStack>
))}
</Box>
  <Button onClick={(_e) => addEvents([Event("state.logout", {})], (_e), {})}>
  {`Sign out`}
</Button>
</VStack>
</Box>
  <Box sx={{"borderX": "1px solid #ededed", "h": "100%"}}>
  <HStack justify={`space-between`} sx={{"p": 4, "borderBottom": "1px solid #ededed"}}>
  <Heading size={`md`}>
  {`Home`}
</Heading>
  <Input onChange={(_e0) => addEvents([Event("state.home_state.set_search", {search:_e0.target.value})], (_e0), {})} placeholder={`Search tweets`} type={`text`}/>
</HStack>
  <Grid sx={{"gridTemplateColumns": "1fr 5fr", "borderBottom": "1px solid #ededed"}}>
  <VStack sx={{"p": 4}}>
  <Avatar size={`md`}/>
</VStack>
  <Box>
  <Textarea onBlur={(_e0) => addEvents([Event("state.home_state.set_tweet", {value:_e0.target.value})], (_e0), {})} placeholder={`What's happening?`} sx={{"w": "100%", "border": 0, "resize": "none", "py": 4, "px": 0, "_focus": {"border": 0, "outline": 0, "boxShadow": "none"}}}/>
  <HStack justifyContent={`flex-end`} sx={{"borderTop": "1px solid #ededed", "px": 4, "py": 2}}>
  <Button onClick={(_e) => addEvents([Event("state.home_state.post_tweet", {})], (_e), {})} sx={{"bg": "rgb(29 161 242)", "color": "white", "borderRadius": "full"}}>
  {`Tweet`}
</Button>
</HStack>
</Box>
</Grid>
  <Fragment>
  {isTrue(state.home_state.tweets) ? (
  <Fragment>
  {state.home_state.tweets.map((myprhxdm, zilebato) => (
  <Grid key={zilebato} sx={{"gridTemplateColumns": "1fr 5fr", "py": 4, "gap": 1, "borderBottom": "1px solid #ededed"}}>
  <VStack>
  <Avatar name={myprhxdm.author} size={`sm`}/>
</VStack>
  <Box>
  <Text sx={{"fontWeight": "bold"}}>
  {("@" + myprhxdm.author)}
</Text>
  <Text sx={{"width": "100%"}}>
  {myprhxdm.content}
</Text>
</Box>
</Grid>
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
  <Input onChange={(_e0) => addEvents([Event("state.home_state.set_friend", {value:_e0.target.value})], (_e0), {})} placeholder={`Search users`} sx={{"width": "100%"}} type={`text`}/>
  {state.home_state.search_users.map((dwgaiddv, kurqttvr) => (
  <VStack key={kurqttvr} sx={{"py": 2, "width": "100%"}}>
  <HStack sx={{"width": "100%"}}>
  <Avatar name={dwgaiddv.username} size={`sm`}/>
  <Text>
  {dwgaiddv.username}
</Text>
  <Spacer/>
  <Button onClick={(_e) => addEvents([Event("state.home_state.follow_user", {username:dwgaiddv.username})], (_e), {})}>
  <AddIcon/>
</Button>
</HStack>
</VStack>
))}
  <Box sx={{"p": 4, "borderRadius": "md", "border": "1px solid #eaeaea", "w": "100%"}}>
  <Heading size={`sm`}>
  {`Following`}
</Heading>
  {state.home_state.following.map((ouvxsvzz, otutlpou) => (
  <VStack key={otutlpou} sx={{"padding": "1em"}}>
  <HStack>
  <Avatar name={ouvxsvzz.followed_username} size={`sm`}/>
  <Text>
  {ouvxsvzz.followed_username}
</Text>
</HStack>
</VStack>
))}
</Box>
</VStack>
</Grid>
</Box>
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
