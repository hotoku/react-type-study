export type Client = {
  id: number;
  name: string;
};

export type Deal = {
  id: number;
  name: string;
  clientId: number;
};

export type ClientWithDeals = Client & { deals: Deal[] };
