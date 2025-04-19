import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface UserState {
  slackConfig: {
    token: string | null;
    email: string | null;
    isVerified: boolean;
  };
  notionConfig: {
    secret: string | null;
    pageId: string | null;
    isVerified: boolean;
  };
  schedulePeriod?: string;
  channels?: string[];
  loading: boolean;
  error: string | null;
}

const initialState: UserState = {
  slackConfig: {
    token: null,
    email: null,
    isVerified: false,
  },
  notionConfig: {
    secret: null,
    pageId: null,
    isVerified: false,
  },
  schedulePeriod: 'daily',
  channels: [],
  loading: false,
  error: null,
};

const userSlice = createSlice({
  name: 'user',
  initialState,
  reducers: {
    setSlackConfig: (state, action: PayloadAction<UserState['slackConfig']>) => {
      state.slackConfig = action.payload;
    },
    setNotionConfig: (state, action: PayloadAction<UserState['notionConfig']>) => {
      state.notionConfig = action.payload;
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.loading = action.payload;
    },
    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload;
    },
    logout: (state) => {
      state.slackConfig = initialState.slackConfig;
      state.notionConfig = initialState.notionConfig;
    },
    setSchedulePeriod: (state, action: PayloadAction<string>) => {
      state.schedulePeriod = action.payload;
    },
    setChannels: (state, action: PayloadAction<string[]>) => {
      state.channels = action.payload;
    },
  },
});

export const {
  setSlackConfig,
  setNotionConfig,
  setLoading,
  setError,
  logout,
  setSchedulePeriod,
  setChannels,
} = userSlice.actions;

export default userSlice.reducer;