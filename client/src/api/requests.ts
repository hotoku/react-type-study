import { validate } from "jsonschema";

import { Client, ClientWithDeals } from "./types";

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
              id: {
                type: "integer",
              },
              name: {
                type: "string",
              },
              client_id: {
                type: "integer",
              },
            },
            required: ["id", "name", "client_id"],
          },
        },
      },
      required: ["id", "name"],
    },
  };
  validate(data, schema, { throwError: true });
  return data as ClientWithDeals[];
}

export async function createClient(client: Partial<Client>): Promise<Client> {
  if (client.name === undefined) {
    throw new Error(`createClient: invalid object, ${client}`);
  }
  const res = await fetch("/clients", {
    method: "post",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(client),
  });
  const data = await res.json();
  console.log("data", data);
  const schema = {
    type: "object",
    properties: {
      id: {
        type: "integer",
      },
      name: {
        type: "string",
      },
    },
    required: ["id", "name"],
  };
  validate(data, schema, { throwError: true });
  return data as Client;
}
