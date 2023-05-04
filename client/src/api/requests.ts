import { validate } from "jsonschema";

import { Client, ClientWithDeals, Deal } from "./types";

export async function getAllClients(): Promise<ClientWithDeals[]> {
  const res = await fetch("/clients");
  const data = await res.json();
  const schema = {
    type: "array",
    items: {
      type: "object",
      properties: {
        id: {
          type: "integer",
        },
        name: {
          type: "string",
        },
        deals: {
          type: "array",
          items: {
            type: "object",
            properties: {
              id: "integer",
              name: "string",
            },
          },
        },
      },
      required: ["id", "name"],
    },
  };
  validate(data, schema, { throwError: true });
  return data as ClientWithDeals[];
}
