'use client';
import * as React from 'react';
import { Container, Stack, Typography } from '@mui/material';
import QuestionComponent from './components/question';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import useMediaQuery from '@mui/material/useMediaQuery';


export default function HomePage() {
  const prefersDarkMode = useMediaQuery('(prefers-color-scheme: dark)');

  const theme = React.useMemo(
    () =>
      createTheme({
        palette: {
          mode: prefersDarkMode ? 'dark' : 'light',
        },
      }),
    [prefersDarkMode],
  );

  return (
    <ThemeProvider theme={theme}>

      <CssBaseline />

      <Container maxWidth="xl" sx={{
        minHeight: '100vw'
      }
      }>
        <Stack spacing={2} >
          <Typography variant="h4" component="h1" gutterBottom>
            LLM Support Bot
          </Typography>
          <QuestionComponent />
        </Stack>
      </Container >
    </ThemeProvider>

  );
}