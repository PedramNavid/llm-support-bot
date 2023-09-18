'use client'
import React, { useState } from 'react';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import { MuiMarkdown, getOverrides } from 'mui-markdown';
import { Highlight, themes } from 'prism-react-renderer';
import { Button, FormControl, FormControlLabel, FormLabel, Grid, Radio, RadioGroup, Typography, styled } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
const host = process.env.NEXT_PUBLIC_API_URL || "http://localhost:3000";
const url = host + "/ask"

const QuestionComponent: React.FC = () => {

    const [question, setQuestion] = useState<string>('');
    const [response, setResponse] = useState<string | null>(null);
    const [selectedModel, setSelectedModel] = useState('gpt3');

    const handleModelChange = (event) => {
        setSelectedModel(event.target.value);
    };

    const handleSubmit = async () => {
        try {
            const requestBody = {
                question: question,
                model: selectedModel
            };
            console.log(requestBody)
            setResponse("Fetching response from llm support bot...");
            const responseRaw = await fetch(url,
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(requestBody)
                });

            if (!responseRaw.ok) {
                throw new Error('Something went wrong');
            }
            const responseJson = await responseRaw.json();
            let txt = responseJson.response;
            console.log(txt);
            txt = txt.replace(/\n/gi, '\n\n');
            setResponse(txt);
        } catch (error) {
            console.error(error)
            setResponse('Something went wrong');
        }
    };

    return (
        <Box>
            <Grid container spacing={4}
            >
                <Grid item xs={8} >
                    <TextField
                        fullWidth
                        minRows={10}
                        multiline
                        placeholder="Paste question here"
                        onChange={(e) => setQuestion(e.target.value)}
                    />
                </Grid>
                <Grid item xs={4}>
                    <FormControl>
                        <FormLabel id="radio-buttons-group-label">Model</FormLabel>
                        <RadioGroup
                            aria-labelledby="radio-buttons-group-label"
                            defaultValue="gpt-3.5"
                            name="radio-buttons-group"
                            value={selectedModel}
                            onChange={handleModelChange}

                        >
                            <FormControlLabel value="gpt3" control={<Radio />} label="GPT-3.5" />
                            <FormControlLabel value="gpt4" control={<Radio />} label="GPT-4" />
                        </RadioGroup>
                    </FormControl>
                </Grid>
                <Grid item xs={3}>
                    <Button variant="outlined" endIcon={<SendIcon />} onClick={handleSubmit}>Ask Question</Button>
                </Grid>
                <Grid item xs={10}>
                    <Box sx={{
                        gap: 4,
                        p: 4,
                        bgcolor: 'background.paper',
                        boxShadow: 1,
                        borderRadius: 4,
                        minHeight: '400px'
                    }}>
                        <Typography variant="body1">Response:</Typography>
                        {response && (
                            <MuiMarkdown
                                Highlight={Highlight}
                                themes={themes}
                                prismTheme={themes.github}
                                overrides={{
                                    ...getOverrides(),
                                    h1: {
                                        component: 'p'
                                    }
                                }}
                            >
                                {response}
                            </MuiMarkdown>
                        )}
                    </Box>

                </Grid>
            </Grid>
        </Box >
    );
}
export const Head = () => <title>LLM Support Bot</title>
export default QuestionComponent;

