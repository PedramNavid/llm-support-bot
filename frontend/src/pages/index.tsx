import * as React from 'react';
import QuestionComponent from './question';
import Container from '@mui/material/Container';
import Box from '@mui/material/Box';
import { Typography } from '@mui/material';
import CssBaseline from '@mui/material/CssBaseline';
const IndexPage = () => {
    return (
        <Container maxWidth="xl">
            <CssBaseline />
            <Box sx={{
                my: 4,
                display: "flex",
                alignItems: "center",
                flexDirection: "column"
            }}>
                <Typography variant="h4" component="h1" gutterBottom>
                    LLM Support Bot
                </Typography>
                <Typography variant="body2" align="center">
                    Ask your question here:
                </Typography>
                <QuestionComponent />
            </Box>
        </Container>
    )
}

export const Head = () => <title>LLM Support Bot</title>

export default IndexPage;

