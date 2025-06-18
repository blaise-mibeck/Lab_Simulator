import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import yaml
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ConfigEditorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title('Lab Config Editor')
        self.config = {}
        self.file_path = ''
        self.create_menu()
        self.create_tabs()

    def create_menu(self):
        menubar = tk.Menu(self.root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label='Open', command=self.open_file)
        filemenu.add_command(label='Save', command=self.save_file)
        filemenu.add_separator()
        filemenu.add_command(label='Exit', command=self.root.quit)
        menubar.add_cascade(label='File', menu=filemenu)
        self.root.config(menu=menubar)

    def create_tabs(self):
        self.tabs = ttk.Notebook(self.root)
        self.equipment_tab = ttk.Frame(self.tabs)
        self.staff_tab = ttk.Frame(self.tabs)
        self.instruments_tab = ttk.Frame(self.tabs)
        self.workflow_tab = ttk.Frame(self.tabs)
        self.simulation_tab = ttk.Frame(self.tabs)
        self.tabs.add(self.equipment_tab, text='Equipment')
        self.tabs.add(self.staff_tab, text='Staff')
        self.tabs.add(self.instruments_tab, text='Instruments')
        self.tabs.add(self.workflow_tab, text='Workflow Steps')
        self.tabs.add(self.simulation_tab, text='Simulation')
        self.tabs.pack(expand=1, fill='both')
        self.create_equipment_tab()
        self.create_staff_tab()
        self.create_instruments_tab()
        self.create_workflow_tab()
        self.create_simulation_tab()

    def create_equipment_tab(self):
        self.eq_listbox = tk.Listbox(self.equipment_tab)
        self.eq_listbox.pack(side='left', fill='y')
        self.eq_listbox.bind('<<ListboxSelect>>', self.on_eq_select)
        btn_frame = tk.Frame(self.equipment_tab)
        btn_frame.pack(side='left', fill='y')
        tk.Button(btn_frame, text='Add', command=self.add_equipment).pack(fill='x')
        tk.Button(btn_frame, text='Edit', command=self.edit_equipment).pack(fill='x')
        tk.Button(btn_frame, text='Delete', command=self.delete_equipment).pack(fill='x')
        self.eq_details = tk.Text(self.equipment_tab, width=60)
        self.eq_details.pack(side='left', fill='both', expand=True)

    def create_staff_tab(self):
        self.staff_listbox = tk.Listbox(self.staff_tab)
        self.staff_listbox.pack(side='left', fill='y')
        self.staff_listbox.bind('<<ListboxSelect>>', self.on_staff_select)
        btn_frame = tk.Frame(self.staff_tab)
        btn_frame.pack(side='left', fill='y')
        tk.Button(btn_frame, text='Add', command=self.add_staff).pack(fill='x')
        tk.Button(btn_frame, text='Edit', command=self.edit_staff).pack(fill='x')
        tk.Button(btn_frame, text='Delete', command=self.delete_staff).pack(fill='x')
        self.staff_details = tk.Text(self.staff_tab, width=60)
        self.staff_details.pack(side='left', fill='both', expand=True)

    def create_instruments_tab(self):
        self.instr_listbox = tk.Listbox(self.instruments_tab)
        self.instr_listbox.pack(side='left', fill='y')
        self.instr_listbox.bind('<<ListboxSelect>>', self.on_instr_select)
        btn_frame = tk.Frame(self.instruments_tab)
        btn_frame.pack(side='left', fill='y')
        tk.Button(btn_frame, text='Add', command=self.add_instrument).pack(fill='x')
        tk.Button(btn_frame, text='Edit', command=self.edit_instrument).pack(fill='x')
        tk.Button(btn_frame, text='Delete', command=self.delete_instrument).pack(fill='x')
        self.instr_details = tk.Text(self.instruments_tab, width=60)
        self.instr_details.pack(side='left', fill='both', expand=True)

    def create_workflow_tab(self):
        self.wf_listbox = tk.Listbox(self.workflow_tab)
        self.wf_listbox.pack(side='left', fill='y')
        self.wf_listbox.bind('<<ListboxSelect>>', self.on_wf_select)
        btn_frame = tk.Frame(self.workflow_tab)
        btn_frame.pack(side='left', fill='y')
        tk.Button(btn_frame, text='Add', command=self.add_workflow_step).pack(fill='x')
        tk.Button(btn_frame, text='Edit', command=self.edit_workflow_step).pack(fill='x')
        tk.Button(btn_frame, text='Delete', command=self.delete_workflow_step).pack(fill='x')
        self.wf_details = tk.Text(self.workflow_tab, width=60)
        self.wf_details.pack(side='left', fill='both', expand=True)

    def create_simulation_tab(self):
        frame = tk.Frame(self.simulation_tab)
        frame.pack(fill='both', expand=True)
        tk.Label(frame, text='Number of Samples:').grid(row=0, column=0)
        self.sim_samples = tk.Entry(frame)
        self.sim_samples.insert(0, '10')
        self.sim_samples.grid(row=0, column=1)
        tk.Button(frame, text='Run Simulation', command=self.run_simulation).grid(row=1, column=0, columnspan=2)
        self.sim_canvas = None

    def open_file(self):
        path = filedialog.askopenfilename(filetypes=[('YAML files', '*.txt *.yaml *.yml')])
        if not path:
            return
        with open(path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f) or {}
        self.file_path = path
        self.refresh_lists()
        messagebox.showinfo('Config Editor', f'Loaded {path}')

    def save_file(self):
        if not self.file_path:
            self.file_path = filedialog.asksaveasfilename(defaultextension='.txt', filetypes=[('YAML files', '*.txt *.yaml *.yml')])
        if not self.file_path:
            return
        with open(self.file_path, 'w', encoding='utf-8') as f:
            yaml.dump(self.config, f, sort_keys=False, allow_unicode=True)
        messagebox.showinfo('Config Editor', f'Saved {self.file_path}')

    def refresh_lists(self):
        self.eq_listbox.delete(0, tk.END)
        for k in (self.config.get('equipment') or {}):
            self.eq_listbox.insert(tk.END, k)
        self.eq_details.delete('1.0', tk.END)
        self.staff_listbox.delete(0, tk.END)
        for k in (self.config.get('staff') or {}):
            self.staff_listbox.insert(tk.END, k)
        self.staff_details.delete('1.0', tk.END)
        self.instr_listbox.delete(0, tk.END)
        for k in (self.config.get('instruments') or {}):
            self.instr_listbox.insert(tk.END, k)
        self.instr_details.delete('1.0', tk.END)
        self.wf_listbox.delete(0, tk.END)
        for k in (self.config.get('workflow_steps') or {}):
            self.wf_listbox.insert(tk.END, k)
        self.wf_details.delete('1.0', tk.END)

    def on_eq_select(self, event):
        sel = self.eq_listbox.curselection()
        if not sel:
            return
        key = self.eq_listbox.get(sel[0])
        eq = self.config.get('equipment', {}).get(key, {})
        self.eq_details.delete('1.0', tk.END)
        self.eq_details.insert(tk.END, yaml.dump(eq, sort_keys=False, allow_unicode=True))

    def on_staff_select(self, event):
        sel = self.staff_listbox.curselection()
        if not sel:
            return
        key = self.staff_listbox.get(sel[0])
        st = self.config.get('staff', {}).get(key, {})
        self.staff_details.delete('1.0', tk.END)
        self.staff_details.insert(tk.END, yaml.dump(st, sort_keys=False, allow_unicode=True))

    def on_instr_select(self, event):
        sel = self.instr_listbox.curselection()
        if not sel:
            return
        key = self.instr_listbox.get(sel[0])
        instr = self.config.get('instruments', {}).get(key, {})
        self.instr_details.delete('1.0', tk.END)
        self.instr_details.insert(tk.END, yaml.dump(instr, sort_keys=False, allow_unicode=True))

    def on_wf_select(self, event):
        sel = self.wf_listbox.curselection()
        if not sel:
            return
        key = self.wf_listbox.get(sel[0])
        wf = self.config.get('workflow_steps', {}).get(key, {})
        self.wf_details.delete('1.0', tk.END)
        self.wf_details.insert(tk.END, yaml.dump(wf, sort_keys=False, allow_unicode=True))

    def add_equipment(self):
        key = simpledialog.askstring('Add Equipment', 'Equipment key (unique):')
        if not key:
            return
        eq = self.edit_equipment_dialog({})
        if eq:
            self.config.setdefault('equipment', {})[key] = eq
            self.refresh_lists()

    def edit_equipment(self):
        sel = self.eq_listbox.curselection()
        if not sel:
            return
        key = self.eq_listbox.get(sel[0])
        eq = self.config.get('equipment', {}).get(key, {})
        new_eq = self.edit_equipment_dialog(eq)
        if new_eq:
            self.config['equipment'][key] = new_eq
            self.refresh_lists()

    def delete_equipment(self):
        sel = self.eq_listbox.curselection()
        if not sel:
            return
        key = self.eq_listbox.get(sel[0])
        if messagebox.askyesno('Delete', f'Delete equipment {key}?'):
            del self.config['equipment'][key]
            self.refresh_lists()

    def add_staff(self):
        key = simpledialog.askstring('Add Staff', 'Staff key (unique):')
        if not key:
            return
        st = self.edit_staff_dialog({})
        if st:
            self.config.setdefault('staff', {})[key] = st
            self.refresh_lists()

    def edit_staff(self):
        sel = self.staff_listbox.curselection()
        if not sel:
            return
        key = self.staff_listbox.get(sel[0])
        st = self.config.get('staff', {}).get(key, {})
        new_st = self.edit_staff_dialog(st)
        if new_st:
            self.config['staff'][key] = new_st
            self.refresh_lists()

    def delete_staff(self):
        sel = self.staff_listbox.curselection()
        if not sel:
            return
        key = self.staff_listbox.get(sel[0])
        if messagebox.askyesno('Delete', f'Delete staff {key}?'):
            del self.config['staff'][key]
            self.refresh_lists()

    def add_instrument(self):
        key = simpledialog.askstring('Add Instrument', 'Instrument key (unique):')
        if not key:
            return
        instr = self.edit_instrument_dialog({})
        if instr:
            self.config.setdefault('instruments', {})[key] = instr
            self.refresh_lists()

    def edit_instrument(self):
        sel = self.instr_listbox.curselection()
        if not sel:
            return
        key = self.instr_listbox.get(sel[0])
        instr = self.config.get('instruments', {}).get(key, {})
        new_instr = self.edit_instrument_dialog(instr)
        if new_instr:
            self.config['instruments'][key] = new_instr
            self.refresh_lists()

    def delete_instrument(self):
        sel = self.instr_listbox.curselection()
        if not sel:
            return
        key = self.instr_listbox.get(sel[0])
        if messagebox.askyesno('Delete', f'Delete instrument {key}?'):
            del self.config['instruments'][key]
            self.refresh_lists()

    def add_workflow_step(self):
        key = simpledialog.askstring('Add Workflow Step', 'Step key (unique):')
        if not key:
            return
        wf = self.edit_workflow_dialog({})
        if wf:
            self.config.setdefault('workflow_steps', {})[key] = wf
            self.refresh_lists()

    def edit_workflow_step(self):
        sel = self.wf_listbox.curselection()
        if not sel:
            return
        key = self.wf_listbox.get(sel[0])
        wf = self.config.get('workflow_steps', {}).get(key, {})
        new_wf = self.edit_workflow_dialog(wf)
        if new_wf:
            self.config['workflow_steps'][key] = new_wf
            self.refresh_lists()

    def delete_workflow_step(self):
        sel = self.wf_listbox.curselection()
        if not sel:
            return
        key = self.wf_listbox.get(sel[0])
        if messagebox.askyesno('Delete', f'Delete workflow step {key}?'):
            del self.config['workflow_steps'][key]
            self.refresh_lists()

    def create_equipment_tab(self):
        self.eq_listbox = tk.Listbox(self.equipment_tab)
        self.eq_listbox.pack(side='left', fill='y')
        self.eq_listbox.bind('<<ListboxSelect>>', self.on_eq_select)
        btn_frame = tk.Frame(self.equipment_tab)
        btn_frame.pack(side='left', fill='y')
        tk.Button(btn_frame, text='Add', command=self.add_equipment).pack(fill='x')
        tk.Button(btn_frame, text='Edit', command=self.edit_equipment).pack(fill='x')
        tk.Button(btn_frame, text='Delete', command=self.delete_equipment).pack(fill='x')
        self.eq_details = tk.Text(self.equipment_tab, width=60)
        self.eq_details.pack(side='left', fill='both', expand=True)

    def create_staff_tab(self):
        self.staff_listbox = tk.Listbox(self.staff_tab)
        self.staff_listbox.pack(side='left', fill='y')
        self.staff_listbox.bind('<<ListboxSelect>>', self.on_staff_select)
        btn_frame = tk.Frame(self.staff_tab)
        btn_frame.pack(side='left', fill='y')
        tk.Button(btn_frame, text='Add', command=self.add_staff).pack(fill='x')
        tk.Button(btn_frame, text='Edit', command=self.edit_staff).pack(fill='x')
        tk.Button(btn_frame, text='Delete', command=self.delete_staff).pack(fill='x')
        self.staff_details = tk.Text(self.staff_tab, width=60)
        self.staff_details.pack(side='left', fill='both', expand=True)

    def create_instruments_tab(self):
        self.instr_listbox = tk.Listbox(self.instruments_tab)
        self.instr_listbox.pack(side='left', fill='y')
        self.instr_listbox.bind('<<ListboxSelect>>', self.on_instr_select)
        btn_frame = tk.Frame(self.instruments_tab)
        btn_frame.pack(side='left', fill='y')
        tk.Button(btn_frame, text='Add', command=self.add_instrument).pack(fill='x')
        tk.Button(btn_frame, text='Edit', command=self.edit_instrument).pack(fill='x')
        tk.Button(btn_frame, text='Delete', command=self.delete_instrument).pack(fill='x')
        self.instr_details = tk.Text(self.instruments_tab, width=60)
        self.instr_details.pack(side='left', fill='both', expand=True)

    def create_workflow_tab(self):
        self.wf_listbox = tk.Listbox(self.workflow_tab)
        self.wf_listbox.pack(side='left', fill='y')
        self.wf_listbox.bind('<<ListboxSelect>>', self.on_wf_select)
        btn_frame = tk.Frame(self.workflow_tab)
        btn_frame.pack(side='left', fill='y')
        tk.Button(btn_frame, text='Add', command=self.add_workflow_step).pack(fill='x')
        tk.Button(btn_frame, text='Edit', command=self.edit_workflow_step).pack(fill='x')
        tk.Button(btn_frame, text='Delete', command=self.delete_workflow_step).pack(fill='x')
        self.wf_details = tk.Text(self.workflow_tab, width=60)
        self.wf_details.pack(side='left', fill='both', expand=True)

    def create_simulation_tab(self):
        frame = tk.Frame(self.simulation_tab)
        frame.pack(fill='both', expand=True)
        tk.Label(frame, text='Number of Samples:').grid(row=0, column=0)
        self.sim_samples = tk.Entry(frame)
        self.sim_samples.insert(0, '10')
        self.sim_samples.grid(row=0, column=1)
        tk.Button(frame, text='Run Simulation', command=self.run_simulation).grid(row=1, column=0, columnspan=2)
        self.sim_canvas = None

    def open_file(self):
        path = filedialog.askopenfilename(filetypes=[('YAML files', '*.txt *.yaml *.yml')])
        if not path:
            return
        with open(path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f) or {}
        self.file_path = path
        self.refresh_lists()
        messagebox.showinfo('Config Editor', f'Loaded {path}')

    def save_file(self):
        if not self.file_path:
            self.file_path = filedialog.asksaveasfilename(defaultextension='.txt', filetypes=[('YAML files', '*.txt *.yaml *.yml')])
        if not self.file_path:
            return
        with open(self.file_path, 'w', encoding='utf-8') as f:
            yaml.dump(self.config, f, sort_keys=False, allow_unicode=True)
        messagebox.showinfo('Config Editor', f'Saved {self.file_path}')

    def refresh_lists(self):
        self.eq_listbox.delete(0, tk.END)
        for k in (self.config.get('equipment') or {}):
            self.eq_listbox.insert(tk.END, k)
        self.eq_details.delete('1.0', tk.END)
        self.staff_listbox.delete(0, tk.END)
        for k in (self.config.get('staff') or {}):
            self.staff_listbox.insert(tk.END, k)
        self.staff_details.delete('1.0', tk.END)
        self.instr_listbox.delete(0, tk.END)
        for k in (self.config.get('instruments') or {}):
            self.instr_listbox.insert(tk.END, k)
        self.instr_details.delete('1.0', tk.END)
        self.wf_listbox.delete(0, tk.END)
        for k in (self.config.get('workflow_steps') or {}):
            self.wf_listbox.insert(tk.END, k)
        self.wf_details.delete('1.0', tk.END)

    def on_eq_select(self, event):
        sel = self.eq_listbox.curselection()
        if not sel:
            return
        key = self.eq_listbox.get(sel[0])
        eq = self.config.get('equipment', {}).get(key, {})
        self.eq_details.delete('1.0', tk.END)
        self.eq_details.insert(tk.END, yaml.dump(eq, sort_keys=False, allow_unicode=True))

    def on_staff_select(self, event):
        sel = self.staff_listbox.curselection()
        if not sel:
            return
        key = self.staff_listbox.get(sel[0])
        st = self.config.get('staff', {}).get(key, {})
        self.staff_details.delete('1.0', tk.END)
        self.staff_details.insert(tk.END, yaml.dump(st, sort_keys=False, allow_unicode=True))

    def on_instr_select(self, event):
        sel = self.instr_listbox.curselection()
        if not sel:
            return
        key = self.instr_listbox.get(sel[0])
        instr = self.config.get('instruments', {}).get(key, {})
        self.instr_details.delete('1.0', tk.END)
        self.instr_details.insert(tk.END, yaml.dump(instr, sort_keys=False, allow_unicode=True))

    def on_wf_select(self, event):
        sel = self.wf_listbox.curselection()
        if not sel:
            return
        key = self.wf_listbox.get(sel[0])
        wf = self.config.get('workflow_steps', {}).get(key, {})
        self.wf_details.delete('1.0', tk.END)
        self.wf_details.insert(tk.END, yaml.dump(wf, sort_keys=False, allow_unicode=True))

    def add_equipment(self):
        key = simpledialog.askstring('Add Equipment', 'Equipment key (unique):')
        if not key:
            return
        eq = self.edit_equipment_dialog({})
        if eq:
            self.config.setdefault('equipment', {})[key] = eq
            self.refresh_lists()

    def edit_equipment(self):
        sel = self.eq_listbox.curselection()
        if not sel:
            return
        key = self.eq_listbox.get(sel[0])
        eq = self.config.get('equipment', {}).get(key, {})
        new_eq = self.edit_equipment_dialog(eq)
        if new_eq:
            self.config['equipment'][key] = new_eq
            self.refresh_lists()

    def delete_equipment(self):
        sel = self.eq_listbox.curselection()
        if not sel:
            return
        key = self.eq_listbox.get(sel[0])
        if messagebox.askyesno('Delete', f'Delete equipment {key}?'):
            del self.config['equipment'][key]
            self.refresh_lists()

    def add_staff(self):
        key = simpledialog.askstring('Add Staff', 'Staff key (unique):')
        if not key:
            return
        st = self.edit_staff_dialog({})
        if st:
            self.config.setdefault('staff', {})[key] = st
            self.refresh_lists()

    def edit_staff(self):
        sel = self.staff_listbox.curselection()
        if not sel:
            return
        key = self.staff_listbox.get(sel[0])
        st = self.config.get('staff', {}).get(key, {})
        new_st = self.edit_staff_dialog(st)
        if new_st:
            self.config['staff'][key] = new_st
            self.refresh_lists()

    def delete_staff(self):
        sel = self.staff_listbox.curselection()
        if not sel:
            return
        key = self.staff_listbox.get(sel[0])
        if messagebox.askyesno('Delete', f'Delete staff {key}?'):
            del self.config['staff'][key]
            self.refresh_lists()

    def add_instrument(self):
        key = simpledialog.askstring('Add Instrument', 'Instrument key (unique):')
        if not key:
            return
        instr = self.edit_instrument_dialog({})
        if instr:
            self.config.setdefault('instruments', {})[key] = instr
            self.refresh_lists()

    def edit_instrument(self):
        sel = self.instr_listbox.curselection()
        if not sel:
            return
        key = self.instr_listbox.get(sel[0])
        instr = self.config.get('instruments', {}).get(key, {})
        new_instr = self.edit_instrument_dialog(instr)
        if new_instr:
            self.config['instruments'][key] = new_instr
            self.refresh_lists()

    def delete_instrument(self):
        sel = self.instr_listbox.curselection()
        if not sel:
            return
        key = self.instr_listbox.get(sel[0])
        if messagebox.askyesno('Delete', f'Delete instrument {key}?'):
            del self.config['instruments'][key]
            self.refresh_lists()

    def add_workflow_step(self):
        key = simpledialog.askstring('Add Workflow Step', 'Step key (unique):')
        if not key:
            return
        wf = self.edit_workflow_dialog({})
        if wf:
            self.config.setdefault('workflow_steps', {})[key] = wf
            self.refresh_lists()

    def edit_workflow_step(self):
        sel = self.wf_listbox.curselection()
        if not sel:
            return
        key = self.wf_listbox.get(sel[0])
        wf = self.config.get('workflow_steps', {}).get(key, {})
        new_wf = self.edit_workflow_dialog(wf)
        if new_wf:
            self.config['workflow_steps'][key] = new_wf
            self.refresh_lists()

    def delete_workflow_step(self):
        sel = self.wf_listbox.curselection()
        if not sel:
            return
        key = self.wf_listbox.get(sel[0])
        if messagebox.askyesno('Delete', f'Delete workflow step {key}?'):
            del self.config['workflow_steps'][key]
            self.refresh_lists()

    def edit_equipment_dialog(self, eq):
        d = tk.Toplevel(self.root)
        d.title('Edit Equipment')
        entries = {}
        fields = [
            ('name', 'Name'), ('make', 'Make'), ('model', 'Model'), ('year', 'Year'),
            ('serial_number', 'Serial Number'), ('mounting_type', 'Mounting Type'),
            ('location', 'Location'), ('automation_level', 'Automation Level'),
            ('sample_handling_type', 'Sample Handling Type'), ('data_output_type', 'Data Output Type'),
            ('requires_supervision', 'Requires Supervision (true/false)'), ('capacity', 'Capacity'),
            ('max_samples_before_maintenance', 'Max Samples Before Maintenance'),
            ('maintenance_duration_hours', 'Maintenance Duration (hours)'),
            ('calibration_frequency_days', 'Calibration Frequency (days)'),
            ('required_operator_skill', 'Required Operator Skill'),
            ('operator_skill_level', 'Operator Skill Level'),
            ('mtbf_hours', 'MTBF (hours)'), ('mttr_hours', 'MTTR (hours)')
        ]
        for i, (k, label) in enumerate(fields):
            tk.Label(d, text=label).grid(row=i, column=0, sticky='e')
            val = str(eq.get(k, ''))
            e = tk.Entry(d)
            e.insert(0, val)
            e.grid(row=i, column=1)
            entries[k] = e
        def ok():
            for k, e in entries.items():
                eq[k] = e.get()
            d.destroy()
        tk.Button(d, text='OK', command=ok).grid(row=len(fields), column=0, columnspan=2)
        d.wait_window()
        return eq

    def edit_staff_dialog(self, st):
        d = tk.Toplevel(self.root)
        d.title('Edit Staff')
        entries = {}
        fields = [
            ('name', 'Name'), ('role', 'Role'), ('experience_years', 'Experience (years)'),
            ('full_time_equivalent', 'FTE'), ('vacation_days_per_year', 'Vacation Days/Year'),
            ('sick_days_per_year', 'Sick Days/Year'), ('training_days_per_year', 'Training Days/Year'),
            ('efficiency_factor', 'Efficiency Factor'), ('error_rate', 'Error Rate')
        ]
        for i, (k, label) in enumerate(fields):
            tk.Label(d, text=label).grid(row=i, column=0, sticky='e')
            val = str(st.get(k, ''))
            e = tk.Entry(d)
            e.insert(0, val)
            e.grid(row=i, column=1)
            entries[k] = e
        def ok():
            for k, e in entries.items():
                st[k] = e.get()
            d.destroy()
        tk.Button(d, text='OK', command=ok).grid(row=len(fields), column=0, columnspan=2)
        d.wait_window()
        return st

    def edit_instrument_dialog(self, instr):
        d = tk.Toplevel(self.root)
        d.title('Edit Instrument')
        entries = {}
        fields = [
            ('name', 'Name'), ('make', 'Make'), ('model', 'Model'), ('year', 'Year'),
            ('serial_number', 'Serial Number'), ('mounting_type', 'Mounting Type'),
            ('location', 'Location'), ('automation_level', 'Automation Level'),
            ('sample_handling_type', 'Sample Handling Type'), ('data_output_type', 'Data Output Type'),
            ('requires_supervision', 'Requires Supervision (true/false)'), ('capacity', 'Capacity'),
            ('max_samples_before_maintenance', 'Max Samples Before Maintenance'),
            ('maintenance_duration_hours', 'Maintenance Duration (hours)'),
            ('calibration_frequency_days', 'Calibration Frequency (days)'),
            ('required_operator_skill', 'Required Operator Skill'),
            ('operator_skill_level', 'Operator Skill Level'),
            ('mtbf_hours', 'MTBF (hours)'), ('mttr_hours', 'MTTR (hours)')
        ]
        for i, (k, label) in enumerate(fields):
            tk.Label(d, text=label).grid(row=i, column=0, sticky='e')
            val = str(instr.get(k, ''))
            e = tk.Entry(d)
            e.insert(0, val)
            e.grid(row=i, column=1)
            entries[k] = e
        def ok():
            for k, e in entries.items():
                instr[k] = e.get()
            d.destroy()
        tk.Button(d, text='OK', command=ok).grid(row=len(fields), column=0, columnspan=2)
        d.wait_window()
        return instr

    def edit_workflow_dialog(self, wf):
        d = tk.Toplevel(self.root)
        d.title('Edit Workflow Step')
        entries = {}
        fields = [
            ('name', 'Name'), ('category', 'Category'), ('duration', 'Duration (min/most_likely/max)'),
            ('unit', 'Unit'), ('equipment_required', 'Equipment Required (comma separated)'),
            ('required_skills', 'Required Skills (comma separated)'),
            ('skill_level', 'Skill Level'), ('inputs', 'Inputs (comma separated)'),
            ('outputs', 'Outputs (comma separated)'), ('can_batch', 'Can Batch (true/false)'),
            ('max_batch_size', 'Max Batch Size'), ('requires_cleanup', 'Requires Cleanup (true/false)'),
            ('external_lab', 'External Lab'), ('dependencies', 'Dependencies (comma separated)')
        ]
        for i, (k, label) in enumerate(fields):
            tk.Label(d, text=label).grid(row=i, column=0, sticky='e')
            val = str(wf.get(k, ''))
            e = tk.Entry(d)
            e.insert(0, val)
            e.grid(row=i, column=1)
            entries[k] = e
        def ok():
            for k, e in entries.items():
                v = e.get()
                if k in ['equipment_required', 'required_skills', 'inputs', 'outputs', 'dependencies']:
                    wf[k] = [x.strip() for x in v.split(',') if x.strip()]
                elif k in ['can_batch', 'requires_cleanup']:
                    wf[k] = v.lower() == 'true'
                elif k == 'duration':
                    # Parse as dict
                    parts = [int(x) for x in v.split('/') if x.strip()]
                    wf[k] = {'min': parts[0], 'most_likely': parts[1], 'max': parts[2]} if len(parts) == 3 else {}
                else:
                    wf[k] = v
            d.destroy()
        tk.Button(d, text='OK', command=ok).grid(row=len(fields), column=0, columnspan=2)
        d.wait_window()
        return wf

    def run_simulation(self):
        # Dummy simulation: generate burn chart data by work type and day
        import random
        num_samples = int(self.sim_samples.get())
        work_types = ['Sample Entry', 'Sample Preparation', 'Measurement', 'Data Analysis', 'Data Review', 'Reporting']
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
        burn_data = {wt: [0]*len(days) for wt in work_types}
        for s in range(num_samples):
            for i, wt in enumerate(work_types):
                day = random.randint(0, len(days)-1)
                burn_data[wt][day] += 1
        # Calculate % total work per day
        total_work = num_samples * len(work_types)
        percent_burn = [sum(burn_data[wt][d] for wt in work_types)/total_work*100 for d in range(len(days))]
        # Plot
        fig, ax = plt.subplots(figsize=(8,4))
        ax.plot(days, percent_burn, marker='o', label='Planned % Work Complete')
        ax.set_ylabel('% Total Work Complete')
        ax.set_xlabel('Day of Week')
        ax.set_title('Burn Chart: Planned Activity')
        ax.legend()
        if self.sim_canvas:
            self.sim_canvas.get_tk_widget().destroy()
        self.sim_canvas = FigureCanvasTkAgg(fig, master=self.simulation_tab)
        self.sim_canvas.draw()
        self.sim_canvas.get_tk_widget().pack(fill='both', expand=True)

if __name__ == '__main__':
    root = tk.Tk()
    app = ConfigEditorGUI(root)
    root.mainloop()
