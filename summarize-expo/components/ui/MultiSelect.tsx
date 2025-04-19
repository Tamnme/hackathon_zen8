import { Ionicons } from '@expo/vector-icons';
import React, { useState } from 'react';
import { Modal, ScrollView, StyleSheet, TouchableOpacity, View } from 'react-native';
import { Text } from './Text';

interface MultiSelectProps {
  values: string[];
  items: Array<{ label: string; value: string }>;
  onSelect: (values: string[]) => void;
  placeholder?: string;
  style?: any;
}

export function MultiSelect({ values, items, onSelect, placeholder = 'Select options', style }: MultiSelectProps) {
  const [visible, setVisible] = useState(false);
  const selectedLabels = items
    .filter(item => values.includes(item.value))
    .map(item => item.label)
    .join(', ');

  return (
    <>
      <TouchableOpacity
        style={[styles.button, style]}
        onPress={() => setVisible(true)}
      >
        <Text
          style={[styles.buttonText, !selectedLabels && styles.placeholder]}
          numberOfLines={1}
          ellipsizeMode="tail"
        >
          {selectedLabels || placeholder}
        </Text>
        <Ionicons name="chevron-down" size={20} color="#666" />
      </TouchableOpacity>

      <Modal
        visible={visible}
        transparent
        animationType="slide"
        onRequestClose={() => setVisible(false)}
      >
        <TouchableOpacity
          style={styles.modalOverlay}
          activeOpacity={1}
          onPress={() => setVisible(false)}
        >
          <View style={styles.modalContent}>
            <View style={styles.modalHeader}>
              <Text variant="h2" style={styles.modalTitle}>{placeholder}</Text>
              <TouchableOpacity onPress={() => setVisible(false)}>
                <Ionicons name="close" size={24} color="#666" />
              </TouchableOpacity>
            </View>

            <ScrollView style={styles.optionsList}>
              {items.map((item) => (
                <TouchableOpacity
                  key={item.value}
                  style={[
                    styles.option,
                    values.includes(item.value) && styles.selectedOption
                  ]}
                  onPress={() => {
                    const newValues = values.includes(item.value)
                      ? values.filter(v => v !== item.value)
                      : [...values, item.value];
                    onSelect(newValues);
                  }}
                >
                  <Text style={[
                    styles.optionText,
                    values.includes(item.value) && styles.selectedOptionText
                  ]}>
                    {item.label}
                  </Text>
                  {values.includes(item.value) && (
                    <Ionicons name="checkmark" size={20} color="#007AFF" />
                  )}
                </TouchableOpacity>
              ))}
            </ScrollView>

            <View style={styles.footer}>
              <TouchableOpacity
                style={styles.doneButton}
                onPress={() => setVisible(false)}
              >
                <Text style={styles.doneButtonText}>Done</Text>
              </TouchableOpacity>
            </View>
          </View>
        </TouchableOpacity>
      </Modal>
    </>
  );
}

const styles = StyleSheet.create({
  button: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: 12,
    backgroundColor: '#fff',
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#E5E5E5',
  },
  buttonText: {
    fontSize: 16,
    color: '#000',
    flex: 1,
    marginRight: 8,
  },
  placeholder: {
    color: '#999',
  },
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    justifyContent: 'flex-end',
  },
  modalContent: {
    backgroundColor: '#fff',
    borderTopLeftRadius: 16,
    borderTopRightRadius: 16,
    maxHeight: '80%',
  },
  modalHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#E5E5E5',
  },
  modalTitle: {
    fontSize: 18,
    fontWeight: '600',
  },
  optionsList: {
    padding: 8,
  },
  option: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: 16,
    borderRadius: 8,
  },
  selectedOption: {
    backgroundColor: '#F5F5F5',
  },
  optionText: {
    fontSize: 16,
    color: '#000',
  },
  selectedOptionText: {
    color: '#007AFF',
    fontWeight: '500',
  },
  footer: {
    padding: 16,
    borderTopWidth: 1,
    borderTopColor: '#E5E5E5',
  },
  doneButton: {
    backgroundColor: '#007AFF',
    padding: 12,
    borderRadius: 8,
    alignItems: 'center',
  },
  doneButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  selectedContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginTop: 8,
    gap: 8,
  },
  selectedTag: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#F5F5F5',
    paddingVertical: 6,
    paddingHorizontal: 10,
    borderRadius: 16,
  },
  selectedTagText: {
    fontSize: 14,
    color: '#000',
    marginRight: 4,
  },
  removeButton: {
    marginLeft: 2,
  },
}); 