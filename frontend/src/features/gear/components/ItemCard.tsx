import { useState } from "react";
import {
  Card,
  Image,
  Text,
  Group,
  Badge,
  Anchor,
  ScrollArea,
  Table,
  Button,
  Box,
  Stack,
  Collapse,
} from "@mantine/core";
import {
  IconExternalLink,
  IconChevronDown,
  IconChevronUp,
} from "@tabler/icons-react";
import type { ProgressionItem } from "../../../lib/api/index";
import { formatPriceOrNA } from "../../../lib/utils/format";

interface ItemCardProps {
  item: ProgressionItem;
  tier: string;
}

export function ItemCard({ item, tier }: ItemCardProps) {
  const [opened, setOpened] = useState(false);

  return (
    <Card
      withBorder
      padding="sm"
      radius="md"
      style={{
        height: "100%",
        transition: "transform 0.2s ease, box-shadow 0.2s ease",
        cursor: "pointer",
      }}
      onMouseEnter={(e) => {
        e.currentTarget.style.transform = "translateY(-4px)";
        e.currentTarget.style.boxShadow = "var(--mantine-shadow-md)";
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.transform = "translateY(0)";
        e.currentTarget.style.boxShadow = "var(--mantine-shadow-sm)";
      }}
    >
      <Group justify="space-between" align="flex-start" mb="xs">
        <Group gap="xs" wrap="nowrap">
          {item.icon_url ? (
            <Image
              src={item.icon_url}
              w={40}
              h={40}
              fit="contain"
              fallbackSrc="https://placehold.co/40?text=?"
            />
          ) : (
            <Box w={40} h={40} bg="gray.2" style={{ borderRadius: 4 }} />
          )}
          <Stack gap={2} style={{ flex: 1, minWidth: 0 }}>
            <Anchor
              href={item.wiki_url}
              target="_blank"
              rel="noopener noreferrer"
              size="sm"
              fw={500}
              style={{ textDecoration: "none" }}
            >
              {item.name}
              <IconExternalLink
                size={12}
                style={{ marginLeft: 4, display: "inline" }}
              />
            </Anchor>
            {item.price !== null && (
              <Text size="xs" c="dimmed" fw={600}>
                {formatPriceOrNA(item.price)} GP
              </Text>
            )}
          </Stack>
        </Group>
        <Badge size="sm" variant="light" color="yellow">
          {tier}
        </Badge>
      </Group>

      {item.not_found && (
        <Badge color="red" size="xs" mb="xs">
          Not in database
        </Badge>
      )}

      {item.stats && (
        <>
          <Button
            variant="subtle"
            size="xs"
            fullWidth
            onClick={() => setOpened(!opened)}
            rightSection={
              opened ? (
                <IconChevronUp size={14} />
              ) : (
                <IconChevronDown size={14} />
              )
            }
            mb="xs"
          >
            {opened ? "Hide" : "Show"} Stats
          </Button>

          <Collapse in={opened}>
            <ScrollArea h={200}>
              <Table striped>
                <Table.Tbody>
                  {item.stats.melee_strength &&
                    item.stats.melee_strength > 0 && (
                      <Table.Tr>
                        <Table.Td>Melee Str</Table.Td>
                        <Table.Td>+{item.stats.melee_strength}</Table.Td>
                      </Table.Tr>
                    )}
                  {item.stats.ranged_strength &&
                    item.stats.ranged_strength > 0 && (
                      <Table.Tr>
                        <Table.Td>Ranged Str</Table.Td>
                        <Table.Td>+{item.stats.ranged_strength}</Table.Td>
                      </Table.Tr>
                    )}
                  {item.stats.magic_damage && item.stats.magic_damage > 0 && (
                    <Table.Tr>
                      <Table.Td>Magic Dmg</Table.Td>
                      <Table.Td>+{item.stats.magic_damage}%</Table.Td>
                    </Table.Tr>
                  )}
                  {item.stats.prayer_bonus !== undefined &&
                    item.stats.prayer_bonus !== 0 && (
                      <Table.Tr>
                        <Table.Td>Prayer</Table.Td>
                        <Table.Td>
                          {item.stats.prayer_bonus > 0 ? "+" : ""}
                          {item.stats.prayer_bonus}
                        </Table.Td>
                      </Table.Tr>
                    )}
                  {item.stats.attack_stab && item.stats.attack_stab > 0 && (
                    <Table.Tr>
                      <Table.Td>Stab</Table.Td>
                      <Table.Td>+{item.stats.attack_stab}</Table.Td>
                    </Table.Tr>
                  )}
                  {item.stats.attack_slash && item.stats.attack_slash > 0 && (
                    <Table.Tr>
                      <Table.Td>Slash</Table.Td>
                      <Table.Td>+{item.stats.attack_slash}</Table.Td>
                    </Table.Tr>
                  )}
                  {item.stats.attack_crush && item.stats.attack_crush > 0 && (
                    <Table.Tr>
                      <Table.Td>Crush</Table.Td>
                      <Table.Td>+{item.stats.attack_crush}</Table.Td>
                    </Table.Tr>
                  )}
                  {item.stats.attack_magic && item.stats.attack_magic > 0 && (
                    <Table.Tr>
                      <Table.Td>Magic</Table.Td>
                      <Table.Td>+{item.stats.attack_magic}</Table.Td>
                    </Table.Tr>
                  )}
                  {item.stats.attack_ranged && item.stats.attack_ranged > 0 && (
                    <Table.Tr>
                      <Table.Td>Ranged</Table.Td>
                      <Table.Td>+{item.stats.attack_ranged}</Table.Td>
                    </Table.Tr>
                  )}
                </Table.Tbody>
              </Table>

              {item.requirements && (
                <Stack gap="xs" mt="xs">
                  <Text size="xs" fw={700} c="dimmed">
                    Requirements:
                  </Text>
                  <Group gap="xs">
                    {item.requirements.attack &&
                      item.requirements.attack > 1 && (
                        <Badge size="xs" variant="outline">
                          Atk {item.requirements.attack}
                        </Badge>
                      )}
                    {item.requirements.strength &&
                      item.requirements.strength > 1 && (
                        <Badge size="xs" variant="outline">
                          Str {item.requirements.strength}
                        </Badge>
                      )}
                    {item.requirements.defence &&
                      item.requirements.defence > 1 && (
                        <Badge size="xs" variant="outline">
                          Def {item.requirements.defence}
                        </Badge>
                      )}
                    {item.requirements.ranged &&
                      item.requirements.ranged > 1 && (
                        <Badge size="xs" variant="outline">
                          Rng {item.requirements.ranged}
                        </Badge>
                      )}
                    {item.requirements.magic && item.requirements.magic > 1 && (
                      <Badge size="xs" variant="outline">
                        Mag {item.requirements.magic}
                      </Badge>
                    )}
                    {item.requirements.quest && (
                      <Badge size="xs" color="orange" variant="light">
                        {item.requirements.quest}
                      </Badge>
                    )}
                  </Group>
                </Stack>
              )}
            </ScrollArea>
          </Collapse>
        </>
      )}
    </Card>
  );
}
