import {
  Button,
  SxProps,
  Theme,
  CircularProgress,
  ButtonProps,
} from "@mui/material";
import { useTranslation } from "react-i18next";
interface propsType
  extends Omit<
    ButtonProps,
    keyof {
      loading: boolean;
      title: string;
      sx?: SxProps<Theme> | undefined;
      disabled?: boolean;
      variant?: "contained" | "outlined" | "text";
      type?: "button" | "reset" | "submit" | undefined;
      onClick?: Function;
    }
  > {
  loading?: boolean;
  title: string;
  sx?: SxProps<Theme> | undefined;
  disabled?: boolean;
  variant?: "contained" | "outlined" | "text";
  type?: "button" | "reset" | "submit" | undefined;
  onClick?: Function;
}

const GenericButton = ({
  loading,
  title,
  sx,
  disabled,
  variant = "contained",
  type,
  onClick,
  ...props
}: propsType) => {
  const { t } = useTranslation("translation");

  return (
    <Button
      onClick={(e) => {
        onClick && onClick(e);
      }}
      type={type}
      variant={variant}
      fullWidth
      disabled={disabled || loading}
      sx={{ p: 1.2, borderRadius: `${12}px`, ...sx }}
      {...props}
    >
      {loading ? <CircularProgress size={28} /> : t(title)}
    </Button>
  );
};

export default GenericButton;
