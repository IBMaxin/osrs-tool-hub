import { useState, useMemo } from 'react';
import { Select } from '@mantine/core';

export interface SearchableDropdownItem {
  value: string;
  label: string;
  group?: string;
}

interface SearchableDropdownProps {
  data: SearchableDropdownItem[];
  value: string | null;
  onChange: (value: string | null) => void;
  placeholder?: string;
  label?: string;
  nothingFoundMessage?: string;
  maxDropdownHeight?: number;
}

const osrsDropdownStyles = {
  dropdown: {
    backgroundColor: '#2B1B0E',
    border: '2px solid #4A360C',
  },
  option: {
    '&[data-combobox-selected], &[data-combobox-active]': {
      backgroundColor: '#4A360C',
    },
  },
};

/**
 * Searchable select with OSRS-themed dropdown. Use for 50+ item lists (e.g. bosses, categories).
 */
export function SearchableDropdown({
  data,
  value,
  onChange,
  placeholder = 'Search...',
  label,
  nothingFoundMessage = 'No results found',
  maxDropdownHeight = 300,
}: SearchableDropdownProps) {
  const [search, setSearch] = useState('');
  const filtered = useMemo(
    () =>
      data.filter((item) =>
        item.label.toLowerCase().includes(search.toLowerCase())
      ),
    [data, search]
  );

  return (
    <Select
      label={label}
      searchable
      searchValue={search}
      onSearchChange={setSearch}
      data={filtered}
      value={value}
      onChange={onChange}
      placeholder={placeholder}
      nothingFoundMessage={nothingFoundMessage}
      maxDropdownHeight={maxDropdownHeight}
      clearable
      styles={osrsDropdownStyles}
    />
  );
}
