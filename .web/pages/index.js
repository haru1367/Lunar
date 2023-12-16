import { Fragment, useContext, useEffect, useRef, useState } from "react"
import { useRouter } from "next/router"
import { Event, getAllLocalStorageItems, getRefValue, getRefValues, isTrue, preventDefault, refs, set_val, spreadArraysOrObjects, uploadFiles, useEventLoop } from "/utils/state"
import { ColorModeContext, EventLoopContext, initialEvents, StateContext } from "/utils/context.js"
import "focus-visible/dist/focus-visible"
import { Avatar, Box, Button, Container, Grid, HStack, Image, Input, Link, Modal, ModalBody, ModalContent, ModalFooter, ModalHeader, ModalOverlay, SimpleGrid, Spacer, Text, Textarea, VStack } from "@chakra-ui/react"
import { getEventURL } from "/utils/state.js"
import { DebounceInput } from "react-debounce-input"
import { AddIcon, RepeatIcon } from "@chakra-ui/icons"
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
  <Image src={`/moon.png`} sx={{"height": "60px", "width": "60px"}}/>
  <Text sx={{"fontSize": "40px", "fontWeight": "bolder", "fontFamily": "Calibri, Calibri", "background": "-webkit-linear-gradient(-45deg, #e04a3f, #4e8be6)", "-webkit-background-clip": "text", "color": "transparent", "centerContent": true}}>
  {`Lunar`}
</Text>
</HStack>
</Container>
  <VStack alignItems={`start`}>
  <Container>
  <HStack>
  <Image src={`/human.png`} sx={{"height": "40px", "width": "40px"}}/>
  <Text sx={{"fontSize": "25px", "fontWeight": "bolder", "fontFamily": "Calibri, Calibri", "background": "-webkit-linear-gradient(-45deg, #8ea6e6, #ad3ce6)", "-webkit-background-clip": "text", "color": "transparent"}}>
  {`Recommended freinds`}
</Text>
</HStack>
  <Container sx={{"height": "10px"}}/>
  <VStack sx={{"border": "2px solid #000000", "borderRadius": "30px"}}>
  <Container sx={{"height": "200px"}}/>
</VStack>
</Container>
</VStack>
  <Button onClick={(_e) => addEvents([Event("state.logout", {})], (_e), {})} sx={{"bg": "#212963", "color": "white", "_hover": {"bg": "blue.600"}}}>
  {`Sign out`}
</Button>
  <Container sx={{"height": "200px"}}/>
</VStack>
</Box>
  <Box sx={{"h": "100%", "borderX": "3px solid #000000", "overflow": "auto"}}>
  <HStack justify={`space-between`} sx={{"p": 4, "borderBottom": "3px solid #000000"}}>
  <Image src={`/find1.png`} sx={{"height": "35px", "width": "35px"}}/>
  <Input onChange={(_e0) => addEvents([Event("state.home_state.set_search", {search:_e0.target.value})], (_e0), {})} placeholder={`Search contents`} type={`text`}/>
</HStack>
  <VStack>
  <Container sx={{"height": "5px"}}/>
  <VStack sx={{"marginLeft": "5px", "width": "97%", "borderRadius": "20px", "border": "3px solid #000000"}}>
  <HStack sx={{"width": "95%", "marginLeft": "30px"}}>
  <Avatar size={`md`}/>
  <Container sx={{"width": "30px"}}/>
  <DebounceInput debounceTimeout={50} element={Textarea} onChange={(_e0) => addEvents([Event("state.home_state.set_crater", {value:_e0.target.value})], (_e0), {})} placeholder={`What's happening?`} sx={{"w": "100%", "border": 2, "resize": "none", "py": 4, "px": 0, "_focus": {"border": 0, "outline": 0, "boxShadow": "none"}}} value={state.home_state.crater}/>
</HStack>
  <HStack justifyContent={`flex-end`} sx={{"px": 4, "py": 2, "width": "100%"}}>
  <Button onClick={(_e) => addEvents([Event("state.home_state.handle_file_selection", {})], (_e), {})} sx={{"borderRadius": "1em"}}>
  <Image src={`/fileselect.png`} sx={{"height": "35px", "width": "35px"}}/>
</Button>
  <Button onClick={(_e) => addEvents([Event("state.home_state.file_select_cancel", {})], (_e), {})} sx={{"borderRadius": "1em"}}>
  <Image src={`/selectcancel.png`} sx={{"height": "35px", "width": "35px"}}/>
</Button>
  <Button onClick={(_e) => addEvents([Event("state.home_state.post_crater", {})], (_e), {})} sx={{"borderRadius": "1em"}}>
  <Image src={`/write.png`} sx={{"height": "30px", "width": "30px"}}/>
</Button>
</HStack>
  <Modal isOpen={state.home_state.imgshow}>
  <ModalOverlay>
  <ModalContent>
  <ModalHeader>
  {`File upload`}
</ModalHeader>
  <ModalBody>
  <SimpleGrid columns={[2]} spacing={`5px`}>
  {state.home_state.img.map((ummwkizj, dylyskmq) => (
  <VStack key={dylyskmq}>
  <Image src={ummwkizj}/>
  <Text>
  {ummwkizj}
</Text>
</VStack>
))}
</SimpleGrid>
</ModalBody>
  <ModalFooter>
  <Button onClick={(_e) => addEvents([Event("state.home_state.change", {})], (_e), {})}>
  {`Confirm`}
</Button>
  <Button onClick={(_e) => addEvents([Event("state.home_state.file_select_cancel", {})], (_e), {})} sx={{"borderRadius": "1em", "boxShadow": "rgba(151, 65, 252, 0.8) 0 15px 30px -10px", "backgroundImage": "linear-gradient(144deg,#AF40FF,#5B42F3 50%,#00DDEB)", "boxSizing": "border-box", "color": "white", "opacity": "0.6", "_hover": {"opacity": 1}}}>
  {`Cancel`}
</Button>
</ModalFooter>
</ModalContent>
</ModalOverlay>
</Modal>
  <SimpleGrid columns={[2]} spacing={`5px`}>
  {state.home_state.img.map((eslwnmda, esoufejc) => (
  <VStack key={esoufejc}>
  <Text>
  {eslwnmda}
</Text>
</VStack>
))}
</SimpleGrid>
</VStack>
</VStack>
  <Container sx={{"height": "10px"}}/>
  <Fragment>
  {isTrue(state.home_state.craters) ? (
  <Fragment>
  {state.home_state.craters.map((yerjgbxg, ieomdcql) => (
  <VStack alignItems={`start`} key={ieomdcql} sx={{"marginLeft": "25px", "width": "auto"}}>
  <HStack>
  <Avatar name={yerjgbxg.author} size={`md`}/>
  <Text sx={{"fontWeight": "bold", "fontSize": "20px"}}>
  {("@" + yerjgbxg.author)}
</Text>
  <Text>
  {(("[" + yerjgbxg.created_at) + "]")}
</Text>
</HStack>
  <HStack sx={{"py": 4, "gap": 1, "width": "98%"}}>
  <Container sx={{"width": "50px"}}/>
  <Box>
  <Fragment>
  {isTrue(yerjgbxg.image_content) ? (
  <Fragment>
  {yerjgbxg.image_content.split(", ").map((xjxlkmhe, ocnjjbdu) => (
  <Image alt={`crater image`} key={ocnjjbdu} src={`/${xjxlkmhe}`} sx={{"maxWidth": "500px"}}/>
))}
</Fragment>
) : (
  <Fragment>
  <Box/>
</Fragment>
)}
</Fragment>
  <Container sx={{"height": "5px"}}/>
  <Text sx={{"width": "100%", "fontSize": "15px"}}>
  {yerjgbxg.content}
</Text>
  <Container sx={{"height": "10px"}}/>
</Box>
</HStack>
  <Container sx={{"height": "5px"}}/>
</VStack>
))}
</Fragment>
) : (
  <Fragment>
  <VStack sx={{"p": 4}}>
  <Button onClick={(_e) => addEvents([Event("state.home_state.get_craters", {})], (_e), {})}>
  <RepeatIcon sx={{"mr": 1}}/>
  <Text>
  {`Click to load story`}
</Text>
</Button>
</VStack>
</Fragment>
)}
</Fragment>
</Box>
  <VStack alignItems={`start`} sx={{"gap": 4, "h": "100%", "py": 4}}>
  <HStack>
  <Image src={`/find2.png`} sx={{"height": "35px", "width": "35px"}}/>
  <Input onChange={(_e0) => addEvents([Event("state.home_state.set_friend", {value:_e0.target.value})], (_e0), {})} placeholder={`Search users`} sx={{"width": "100%", "border": "3px solid #000000"}} type={`text`}/>
</HStack>
  <Container sx={{"height": "10px"}}/>
  {state.home_state.search_users.map((ffjseweo, xjjhndhg) => (
  <VStack key={xjjhndhg} sx={{"py": 2, "width": "100%"}}>
  <HStack sx={{"width": "100%"}}>
  <Avatar name={ffjseweo.username} size={`sm`}/>
  <Text>
  {ffjseweo.username}
</Text>
  <Spacer/>
  <Button onClick={(_e) => addEvents([Event("state.home_state.follow_user", {username:ffjseweo.username})], (_e), {})}>
  <AddIcon/>
</Button>
</HStack>
</VStack>
))}
</VStack>
</Grid>
  <HStack sx={{"marginRight": "5px", "border": "1px solid #000000", "borderRadius": "full"}}>
  <Link as={NextLink} href={`/`} sx={{"display": "inline-flex", "alignItems": "center", "py": 3, "px": 2}}>
  <Image src={`/Home.png`} sx={{"height": "40px", "width": "40px"}}/>
</Link>
  <Link as={NextLink} href={`/profile`} sx={{"display": "inline-flex", "alignItems": "center", "py": 3, "px": 2}}>
  <Image src={`/profile.png`} sx={{"height": "40px", "width": "40px"}}/>
</Link>
  <Link as={NextLink} href={`/map`} sx={{"display": "inline-flex", "alignItems": "center", "py": 3, "px": 2}}>
  <Image src={`/map.png`} sx={{"height": "40px", "width": "40px"}}/>
</Link>
  <Link as={NextLink} href={`/chat`} sx={{"display": "inline-flex", "alignItems": "center", "py": 3, "px": 2}}>
  <Image src={`/chat.png`} sx={{"height": "40px", "width": "40px"}}/>
</Link>
  <Link as={NextLink} href={`/aichat`} sx={{"display": "inline-flex", "alignItems": "center", "py": 3, "px": 2}}>
  <Image src={`/Aichat.png`} sx={{"height": "40px", "width": "40px"}}/>
</Link>
  <Link as={NextLink} href={`/diary`} sx={{"display": "inline-flex", "alignItems": "center", "py": 3, "px": 2}}>
  <Image src={`/diary.png`} sx={{"height": "40px", "width": "40px"}}/>
</Link>
  <Link as={NextLink} href={`/video`} sx={{"display": "inline-flex", "alignItems": "center", "py": 3, "px": 2}}>
  <Image src={`/video.png`} sx={{"height": "40px", "width": "40px"}}/>
</Link>
  <Link as={NextLink} href={`/game`} sx={{"display": "inline-flex", "alignItems": "center", "py": 3, "px": 2}}>
  <Image src={`/game.png`} sx={{"height": "40px", "width": "40px"}}/>
</Link>
  <Link as={NextLink} href={`/setting`} sx={{"display": "inline-flex", "alignItems": "center", "py": 3, "px": 2}}>
  <Image src={`/setting.png`} sx={{"height": "40px", "width": "40px"}}/>
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
