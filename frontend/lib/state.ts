import { create } from "zustand";

type State = { sector?: string; exchange?: string; priceBand?: [number, number] | null };
type Actions = { setSector: (s?:string)=>void; setExchange:(e?:string)=>void; setPriceBand:(b:[number,number]|null)=>void };

export const useFilters = create<State & Actions>((set) => ({
  sector: undefined,
  exchange: undefined,
  priceBand: null,
  setSector: (sector) => set({ sector }),
  setExchange: (exchange) => set({ exchange }),
  setPriceBand: (priceBand) => set({ priceBand }),
}));
