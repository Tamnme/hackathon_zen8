import AsyncStorage from '@react-native-async-storage/async-storage';
import { configureStore } from '@reduxjs/toolkit';
import { TypedUseSelectorHook, useDispatch, useSelector } from 'react-redux';
import { FLUSH, PAUSE, PERSIST, persistReducer, persistStore, PURGE, REGISTER, REHYDRATE } from 'redux-persist';
import createWebStorage from 'redux-persist/lib/storage/createWebStorage';
import userReducer from './slices/userSlice';

// Create a web storage engine that uses localStorage
const createNoopStorage = () => {
  return {
    getItem(_key: string) {
      return Promise.resolve(null);
    },
    setItem(_key: string, value: string) {
      return Promise.resolve(value);
    },
    removeItem(_key: string) {
      return Promise.resolve();
    }
  };
};

// Create a custom storage engine for web
const createCustomWebStorage = () => {
  // Check if window is defined (web) or not (React Native)
  if (typeof window !== 'undefined' && window.localStorage) {
    // Use localStorage for web
    return createWebStorage('local');
  }
  // Return a noop storage for SSR
  return createNoopStorage();
};

// Storage engine to use based on platform
const storage = typeof window !== 'undefined'
  ? createCustomWebStorage()
  : AsyncStorage;

// Configuration for redux-persist
const persistConfig = {
  key: 'root',
  storage,
  // Add any reducers you want to persist
  whitelist: ['user'],
  // Add any reducers you want to exclude from persistence
  blacklist: [],
};

// Create persisted reducer
const persistedReducer = persistReducer(persistConfig, userReducer);

export const store = configureStore({
  reducer: {
    user: persistedReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: [FLUSH, REHYDRATE, PAUSE, PERSIST, PURGE, REGISTER],
      },
    }),
});

// Create persistor
export const persistor = persistStore(store);

// Infer the `RootState` and `AppDispatch` types from the store itself
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

// Use throughout your app instead of plain `useDispatch` and `useSelector`
export const useAppDispatch = () => useDispatch<AppDispatch>();
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;