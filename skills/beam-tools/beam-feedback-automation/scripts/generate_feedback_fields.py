#!/usr/bin/env python3
"""
Feedback Field Generator
Smart logic to generate appropriate feedback fields based on agent output schema.
"""

import json
import argparse
import sys
from typing import Dict, List, Any
from pathlib import Path


class FeedbackFieldGenerator:
    """Generates feedback fields based on agent output schema."""

    def __init__(self, schema: Dict[str, Any]):
        """Initialize generator with agent schema."""
        self.schema = schema
        self.feedback_fields = []

    def generate(self) -> List[Dict[str, Any]]:
        """Generate feedback fields for all agent outputs."""
        outputs = self.schema.get('outputs', [])

        if not outputs:
            print("⚠️  Warning: No outputs found in schema. Cannot generate feedback fields.")
            return []

        print(f"\n🎯 Generating feedback fields for {len(outputs)} outputs...")

        for output in outputs:
            field_name = output['name']
            field_type = output['type']

            print(f"\n   Analyzing: {field_name} ({field_type})")

            # Apply smart field generation logic based on type
            if field_type == 'number':
                self._generate_number_fields(output)
            elif field_type == 'array':
                self._generate_array_fields(output)
            elif field_type == 'string' or field_type == 'text':
                self._generate_text_fields(output)
            elif field_type == 'boolean':
                self._generate_boolean_fields(output)
            elif field_type == 'object':
                self._generate_object_fields(output)
            else:
                # Default: generic feedback field
                self._generate_generic_fields(output)

        return self.feedback_fields

    def _generate_number_fields(self, output: Dict[str, Any]):
        """Generate feedback fields for number outputs (e.g., scores)."""
        field_name = output['name']

        # Check if it's a score (common pattern)
        is_score = 'score' in field_name.lower() or 'rating' in field_name.lower()

        if is_score:
            # Accuracy rating
            self.feedback_fields.append({
                "name": f"{field_name}_accuracy",
                "label": f"{self._format_label(field_name)} Accuracy",
                "type": "rating",
                "scale": 5,
                "description": f"How accurate is the {field_name}? (1=Very Inaccurate, 5=Very Accurate)"
            })
        else:
            # Correctness for other numbers
            self.feedback_fields.append({
                "name": f"{field_name}_correct",
                "label": f"{self._format_label(field_name)} Correct?",
                "type": "select",
                "options": ["Yes", "No", "Partially"],
                "description": f"Is the {field_name} value correct?"
            })

        # Comments
        self.feedback_fields.append({
            "name": f"{field_name}_comments",
            "label": f"{self._format_label(field_name)} Comments",
            "type": "text",
            "description": f"Additional feedback on {field_name}"
        })

        print(f"      ✓ Generated 2 fields (accuracy/correct + comments)")

    def _generate_array_fields(self, output: Dict[str, Any]):
        """Generate feedback fields for array outputs (e.g., lists of skills)."""
        field_name = output['name']

        # Extraction accuracy
        self.feedback_fields.append({
            "name": f"{field_name}_extraction_accuracy",
            "label": f"{self._format_label(field_name)} Extraction Accuracy",
            "type": "rating",
            "scale": 5,
            "description": f"How accurate is the extraction of {field_name}? (1=Very Inaccurate, 5=Very Accurate)"
        })

        # Missing items
        self.feedback_fields.append({
            "name": f"{field_name}_missing",
            "label": f"Missing {self._format_label(field_name)}",
            "type": "checkbox_list",
            "description": f"What {field_name} were missed by the agent?"
        })

        # Incorrect items
        self.feedback_fields.append({
            "name": f"{field_name}_incorrect",
            "label": f"Incorrect {self._format_label(field_name)}",
            "type": "checkbox_list",
            "description": f"What {field_name} were incorrectly identified?"
        })

        print(f"      ✓ Generated 3 fields (extraction accuracy + missing + incorrect)")

    def _generate_text_fields(self, output: Dict[str, Any]):
        """Generate feedback fields for text outputs (e.g., summaries, descriptions)."""
        field_name = output['name']

        # Quality rating
        self.feedback_fields.append({
            "name": f"{field_name}_quality",
            "label": f"{self._format_label(field_name)} Quality",
            "type": "rating",
            "scale": 5,
            "description": f"Rate the quality of {field_name} (1=Poor, 5=Excellent)"
        })

        # Accuracy
        self.feedback_fields.append({
            "name": f"{field_name}_accuracy",
            "label": f"{self._format_label(field_name)} Accuracy",
            "type": "select",
            "options": ["Accurate", "Partially Accurate", "Inaccurate"],
            "description": f"Is the {field_name} factually accurate?"
        })

        # Comments
        self.feedback_fields.append({
            "name": f"{field_name}_comments",
            "label": f"{self._format_label(field_name)} Comments",
            "type": "text",
            "description": f"Additional feedback on {field_name}"
        })

        print(f"      ✓ Generated 3 fields (quality + accuracy + comments)")

    def _generate_boolean_fields(self, output: Dict[str, Any]):
        """Generate feedback fields for boolean outputs."""
        field_name = output['name']

        # Correctness
        self.feedback_fields.append({
            "name": f"{field_name}_correct",
            "label": f"{self._format_label(field_name)} Correct?",
            "type": "select",
            "options": ["Yes", "No"],
            "description": f"Is the {field_name} decision correct?"
        })

        # Comments
        self.feedback_fields.append({
            "name": f"{field_name}_comments",
            "label": f"{self._format_label(field_name)} Comments",
            "type": "text",
            "description": f"Explain why {field_name} is correct/incorrect"
        })

        print(f"      ✓ Generated 2 fields (correct + comments)")

    def _generate_object_fields(self, output: Dict[str, Any]):
        """Generate feedback fields for object outputs (structured data)."""
        field_name = output['name']

        # Overall accuracy
        self.feedback_fields.append({
            "name": f"{field_name}_accuracy",
            "label": f"{self._format_label(field_name)} Accuracy",
            "type": "rating",
            "scale": 5,
            "description": f"Overall accuracy of {field_name} (1=Very Inaccurate, 5=Very Accurate)"
        })

        # Comments
        self.feedback_fields.append({
            "name": f"{field_name}_comments",
            "label": f"{self._format_label(field_name)} Comments",
            "type": "text",
            "description": f"Feedback on {field_name} structure and content"
        })

        print(f"      ✓ Generated 2 fields (accuracy + comments)")

    def _generate_generic_fields(self, output: Dict[str, Any]):
        """Generate generic feedback fields for unknown types."""
        field_name = output['name']

        # Generic rating
        self.feedback_fields.append({
            "name": f"{field_name}_rating",
            "label": f"{self._format_label(field_name)} Rating",
            "type": "rating",
            "scale": 5,
            "description": f"Rate the {field_name} (1=Poor, 5=Excellent)"
        })

        # Comments
        self.feedback_fields.append({
            "name": f"{field_name}_comments",
            "label": f"{self._format_label(field_name)} Comments",
            "type": "text",
            "description": f"Feedback on {field_name}"
        })

        print(f"      ✓ Generated 2 fields (rating + comments)")

    def _format_label(self, field_name: str) -> str:
        """Format field name into human-readable label."""
        # Replace underscores with spaces and title case
        return field_name.replace('_', ' ').title()

    def add_overall_fields(self):
        """Add overall feedback fields that apply to all agents."""
        print(f"\n   Adding overall feedback fields...")

        # Overall quality
        self.feedback_fields.append({
            "name": "overall_quality",
            "label": "Overall Quality",
            "type": "rating",
            "scale": 5,
            "description": "Overall quality of the agent's output (1=Poor, 5=Excellent)"
        })

        # Overall comments
        self.feedback_fields.append({
            "name": "overall_comments",
            "label": "Overall Comments",
            "type": "text",
            "description": "General feedback and suggestions for improvement"
        })

        # Reviewer name/email
        self.feedback_fields.append({
            "name": "reviewer_email",
            "label": "Reviewer Email",
            "type": "email",
            "description": "Your email address"
        })

        print(f"      ✓ Generated 3 overall fields")

    def save_fields(self, output_dir: str = "analysis") -> str:
        """Save generated feedback fields to JSON file."""
        # Create analysis directory
        analysis_dir = Path(output_dir)
        analysis_dir.mkdir(exist_ok=True)

        # Save fields
        agent_id = self.schema['agent_id']
        output_file = analysis_dir / f"{agent_id}_feedback_fields.json"

        output_data = {
            "agent_id": agent_id,
            "agent_name": self.schema['agent_name'],
            "generated_at": self._get_timestamp(),
            "total_fields": len(self.feedback_fields),
            "fields": self.feedback_fields
        }

        with open(output_file, 'w') as f:
            json.dump(output_data, f, indent=2)

        return str(output_file)

    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().isoformat()

    def display_summary(self):
        """Display summary of generated feedback fields."""
        print(f"\n✅ Feedback Field Generation Complete")
        print(f"\n📊 Generated {len(self.feedback_fields)} feedback fields:")

        for field in self.feedback_fields[:10]:  # Show first 10
            print(f"\n   ✓ {field['label']}")
            print(f"      Type: {field['type']}")
            print(f"      Description: {field['description']}")

        if len(self.feedback_fields) > 10:
            print(f"\n   ... and {len(self.feedback_fields) - 10} more fields")

        print("\n💡 Ready to create Apps Script template!")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description='Generate feedback fields from agent schema')
    parser.add_argument('--schema', required=True, help='Path to agent schema JSON file')
    parser.add_argument('--output-dir', default='analysis', help='Output directory for feedback fields')
    parser.add_argument('--skip-overall', action='store_true', help='Skip overall feedback fields')

    args = parser.parse_args()

    try:
        # Load schema
        with open(args.schema, 'r') as f:
            schema = json.load(f)

        # Generate feedback fields
        generator = FeedbackFieldGenerator(schema)
        fields = generator.generate()

        if not args.skip_overall:
            generator.add_overall_fields()

        # Display summary
        generator.display_summary()

        # Save fields
        output_file = generator.save_fields(args.output_dir)
        print(f"\n💾 Feedback fields saved to: {output_file}")

    except FileNotFoundError:
        print(f"❌ Error: Schema file not found: {args.schema}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"❌ Error: Invalid JSON in schema file: {args.schema}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
