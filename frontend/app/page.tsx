'use client';
import * as React from 'react';
import { Container, Stack, ThemeProvider, Typography, createTheme } from '@mui/material';
import QuestionComponent from './components/question';
import lightThemeOptions from '../styles/theme/lightThemeOptions';

const lightTheme = createTheme(lightThemeOptions);

export default function HomePage() {
  return (
    <ThemeProvider theme={lightTheme}>
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
      </Container ></ThemeProvider>
  );
}