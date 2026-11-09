/*
 * Decompiled with CFR 0.152.
 */
package plus;

import automata.Automaton;
import automata.State;
import automata.Transition;
import gui.editor.EditorPane;
import gui.editor.ToolBar;
import java.awt.Rectangle;
import gui.environment.AutomatonEnvironment;
import gui.environment.Environment;
import gui.environment.EnvironmentFrame;
import java.awt.Component;
import java.awt.Container;
import java.awt.KeyEventDispatcher;
import java.awt.KeyboardFocusManager;
import java.awt.Toolkit;
import java.awt.Window;
import java.awt.event.KeyEvent;
import java.util.ArrayList;
import java.util.List;
import javax.swing.AbstractButton;
import javax.swing.text.JTextComponent;
import plus.Theme;

public class JFLAPPlus {
    public static void main(String[] stringArray) {
        java.util.Locale.setDefault(new java.util.Locale("es", "MX"));
        javax.swing.JComponent.setDefaultLocale(java.util.Locale.getDefault());
        Theme.apply(Theme.savedPreference(), false);
        KeyboardFocusManager.getCurrentKeyboardFocusManager().addKeyEventDispatcher(new KeyEventDispatcher(){

            @Override
            public boolean dispatchKeyEvent(KeyEvent keyEvent) {
                try {
                    return JFLAPPlus.handle(keyEvent);
                }
                catch (Throwable throwable) {
                    throwable.printStackTrace();
                    return false;
                }
            }
        });
        try {
            Class.forName("JFLAP").getMethod("main", String[].class).invoke(null, new Object[]{stringArray});
        }
        catch (Exception exception) {
            exception.printStackTrace();
        }
    }

    static boolean handle(KeyEvent keyEvent) {
        boolean bl;
        if (keyEvent.getID() != 401) {
            return false;
        }
        if ((keyEvent.getKeyCode() == KeyEvent.VK_DELETE || keyEvent.getKeyCode() == KeyEvent.VK_BACK_SPACE)
                && (keyEvent.getModifiersEx() & (KeyEvent.CTRL_DOWN_MASK | KeyEvent.ALT_DOWN_MASK | KeyEvent.META_DOWN_MASK)) == 0) {
            return JFLAPPlus.deleteSelection();
        }
        int n = Toolkit.getDefaultToolkit().getMenuShortcutKeyMaskEx();
        int n2 = keyEvent.getModifiersEx();
        boolean bl2 = bl = (n2 & n) != 0 && (n2 & 0x200) == 0;
        if (!bl) {
            return false;
        }
        boolean bl3 = (n2 & 0x40) != 0;
        int n3 = keyEvent.getKeyCode();
        if (bl3 && n3 == 68) {
            Theme.toggle();
            return true;
        }
        if (bl3 && n3 == KeyEvent.VK_T) {
            Window active = KeyboardFocusManager.getCurrentKeyboardFocusManager().getActiveWindow();
            if (active instanceof EnvironmentFrame) {
                EditorPane editor = JFLAPPlus.findEditor(active);
                if (editor != null && editor.getAutomaton() instanceof automata.turing.TuringMachine) {
                    RuleTable.open(editor);
                    return true;
                }
            }
            return false;
        }
        Window window = KeyboardFocusManager.getCurrentKeyboardFocusManager().getActiveWindow();
        if (!(window instanceof EnvironmentFrame)) {
            return false;
        }
        Component component = KeyboardFocusManager.getCurrentKeyboardFocusManager().getFocusOwner();
        boolean bl4 = component instanceof JTextComponent;
        if (n3 == 90 && !bl4) {
            if (bl3) {
                return JFLAPPlus.redo((EnvironmentFrame)window);
            }
            return JFLAPPlus.undo((EnvironmentFrame)window);
        }
        if (n3 == 89 && !bl3 && !bl4) {
            return JFLAPPlus.redo((EnvironmentFrame)window);
        }
        if (!bl3 && n3 >= 49 && n3 <= 57) {
            return JFLAPPlus.pickTool(window, n3 - 49);
        }
        return false;
    }

    /** Supr / Delete: borra todos los estados y transiciones seleccionados del editor visible. */
    static boolean deleteSelection() {
        Window window = KeyboardFocusManager.getCurrentKeyboardFocusManager().getActiveWindow();
        if (!(window instanceof EnvironmentFrame)) {
            return false;
        }
        Component focus = KeyboardFocusManager.getCurrentKeyboardFocusManager().getFocusOwner();
        if (focus instanceof JTextComponent || focus instanceof javax.swing.JTable || focus instanceof javax.swing.JComboBox) {
            return false;
        }
        EditorPane pane = JFLAPPlus.findEditor(window);
        if (pane == null) {
            return false;
        }
        Automaton automaton = pane.getAutomaton();
        ArrayList<Transition> transitions = new ArrayList<Transition>();
        for (Transition t : automaton.getTransitions()) {
            if (t.isSelected) {
                transitions.add(t);
            }
        }
        ArrayList<State> states = new ArrayList<State>();
        for (State s : automaton.getStates()) {
            if (s.isSelected()) {
                states.add(s);
            }
        }
        if (transitions.isEmpty() && states.isEmpty()) {
            return false;
        }
        AutomatonEnvironment environment = JFLAPPlus.env((EnvironmentFrame)window);
        if (environment != null) {
            environment.saveStatus();
        }
        for (Transition t : transitions) {
            automaton.removeTransition(t);
        }
        for (State s : states) {
            automaton.removeState(s);
        }
        pane.getDrawer().setSelectionBounds(new Rectangle(0, 0, -1, -1));
        pane.getAutomatonPane().repaint();
        return true;
    }

    private static EditorPane findEditor(Container container) {
        for (Component component : container.getComponents()) {
            if (component instanceof EditorPane && component.isShowing()) {
                return (EditorPane)component;
            }
            if (!(component instanceof Container)) continue;
            EditorPane found = JFLAPPlus.findEditor((Container)component);
            if (found != null) {
                return found;
            }
        }
        return null;
    }

    private static AutomatonEnvironment env(EnvironmentFrame environmentFrame) {
        Environment environment = environmentFrame.getEnvironment();
        return environment instanceof AutomatonEnvironment ? (AutomatonEnvironment)environment : null;
    }

    private static boolean undo(EnvironmentFrame environmentFrame) {
        AutomatonEnvironment automatonEnvironment = JFLAPPlus.env(environmentFrame);
        if (automatonEnvironment == null) {
            return false;
        }
        automatonEnvironment.restoreStatus();
        environmentFrame.repaint();
        return true;
    }

    private static boolean redo(EnvironmentFrame environmentFrame) {
        AutomatonEnvironment automatonEnvironment = JFLAPPlus.env(environmentFrame);
        if (automatonEnvironment == null) {
            return false;
        }
        automatonEnvironment.redo();
        environmentFrame.repaint();
        return true;
    }

    private static boolean pickTool(Window window, int n) {
        ArrayList<ToolBar> arrayList = new ArrayList<ToolBar>();
        JFLAPPlus.collect(window, arrayList);
        for (ToolBar toolBar : arrayList) {
            ArrayList<AbstractButton> arrayList2 = new ArrayList<AbstractButton>();
            for (Component component : toolBar.getComponents()) {
                if (!(component instanceof AbstractButton)) continue;
                arrayList2.add((AbstractButton)component);
            }
            if (n >= arrayList2.size()) continue;
            ((AbstractButton)arrayList2.get(n)).doClick();
            return true;
        }
        return false;
    }

    private static void collect(Container container, List<ToolBar> list) {
        for (Component component : container.getComponents()) {
            if (component instanceof ToolBar && component.isShowing()) {
                list.add((ToolBar)component);
            }
            if (!(component instanceof Container)) continue;
            JFLAPPlus.collect((Container)component, list);
        }
    }
}

