import React, { useState } from 'react';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import { MuiMarkdown, getOverrides } from 'mui-markdown';
import { Highlight, themes } from 'prism-react-renderer';

const QuestionComponent: React.FC = () => {
    const [question, setQuestion] = useState<string>('');
    const [response, setResponse] = useState<string | null>(null);

    const handleSubmit = async () => {
        try {
            const requestBody = {
                question: question
            };

            let url = `${process.env.GATSBY_API_URL}/ask`

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

            setResponse("Fetching response from llm support bot...");
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
        <Box sx={{
            marginTop: 8,
            width: 700
        }} >
            <TextField
                fullWidth
                multiline
                rows={10}
                onChange={(e) => setQuestion(e.target.value)}
            />
            <button onClick={handleSubmit}>Submit</button>
            {response && <div><strong>Response:</strong>

                <MuiMarkdown
                    Highlight={Highlight}
                    themes={themes}
                    prismTheme={themes.github}
                    overrides={{
                        ...getOverrides(),
                        h1: {
                            component: 'p'
                        }
                    }}>
                    {response}
                </MuiMarkdown>
            </div>}
        </Box >
    );
}

export const Head = () => <title>LLM Support Bot</title>
export default QuestionComponent;

